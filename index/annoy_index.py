import sqlite3

import annoy
import lmdb
import sent2vec
import logging
import numpy as np
import time
import os
import glob
import re

from nltk.corpus import stopwords
from pathlib import Path
from typing import List, Tuple
from abc import ABCMeta, abstractmethod
from utils.utils import split_compounds
from bert.bert import BertEncoder

# 24 GB Karten: 0, 1
# os.environ['CUDA_VISIBLE_DEVICES'] = "1"
log = logging.getLogger(__name__)


class AnnoyIndexer(metaclass=ABCMeta):
    def __init__(self, embedding_model, embedding_vector_size, metric):
        self._annoy_index = None
        self._annoy_entity_mapping = None
        self._annoy_sentence_mapping = None
        self._metric = metric

        self._embedding_model = embedding_model
        self._embedding_vector_size = embedding_vector_size

    @abstractmethod
    def _get_embedding(self, phrase: str, sentence: str = "") -> Tuple[List[float], bool]:
        pass

    @abstractmethod
    def _create_entity_index(self, context_data: List[sqlite3.Row]):
        pass

    def _check_directory(self, output_filename):
        dirname = os.path.dirname(output_filename)
        if len(dirname) == 0:
            dirname = "."
        if len(glob.glob(os.path.join(dirname, '*.ann'))) > 10:
            log.warning("There are a lot of annoy indice and lmdb mapping files in %s. Make sure to empty the directory"
                        "if necessary." % dirname)
            input("Waiting for keypress to continue...")

    def create_entity_index(self, context_data: List[sqlite3.Row], output_filename: str, num_trees: int=30):
        """
        The public create entity index method that users can call.
        The basic structure is the same but the entity embedding collection is different for every embedding model
        and has to be implemented explicitly using the private _create_entity_index method.
        """
        self._check_directory(output_filename)

        # Note: the timestamp is necessary to prevent the lmdb file to be overwritten
        timestamp = str(time.time())
        file_annoy = output_filename + "_" + timestamp + ".ann"
        file_entity_lmdb = output_filename + "_entity_" + timestamp + ".lmdb"
        file_sentence_lmdb = output_filename + "_sentence_" + timestamp + ".lmdb"

        # Create AnnoyIndex instance
        self._annoy_index = annoy.AnnoyIndex(self._embedding_vector_size, metric=self._metric)

        # Create mapping instance
        self._annoy_entity_mapping = lmdb.open(file_entity_lmdb, map_size=int(1e9))
        self._annoy_sentence_mapping = lmdb.open(file_sentence_lmdb, map_size=int(1e9))

        # Retrieve entity embeddings and add them to the annoy index
        self._create_entity_index(context_data)

        # Build annoy index
        log.info("Building annoy index now.")
        start = time.time()
        self._annoy_index.build(num_trees)
        log.info("Building annoy index took %s" % (time.time() - start))

        # Save annoy index
        self._annoy_index.save(file_annoy)

    def load_entity_index(self, file_annoy: str):
        """
        Load an annoy index and the corresponding lmdb mapping.

        :param file_annoy: 'path/filename.ann'
        """
        file_tmp = (".".join(file_annoy.split(".")[:-1])).split("_")
        file_entity_lmdb = "_".join(file_tmp[:-1]) + "_entity_" + file_tmp[-1] + ".lmdb"
        file_sentence_lmdb = "_".join(file_tmp[:-1]) + "_sentence_" + file_tmp[-1] + ".lmdb"
        assert Path(file_annoy).is_file(), "The annoy file could not be found. Make sure the path is correct."
        assert Path(file_entity_lmdb).is_dir(), "The entity lmdb mapping could not be found. Make sure it is in the same " \
                                                "directory as the .ann file and has the same file name except for " \
                                                "the file extension (.lmdb)."
        assert Path(file_sentence_lmdb).is_dir(), "The sentence lmdb mapping could not be found. Make sure it is in the same " \
                                                  "directory as the .ann file and has the same file name except for " \
                                                  "the file extension (.lmdb)."

        self._annoy_index = annoy.AnnoyIndex(self._embedding_vector_size, metric=self._metric)
        self._annoy_index.load(file_annoy)

        self._annoy_entity_mapping = lmdb.open(file_entity_lmdb, map_size=int(1e9))
        self._annoy_sentence_mapping = lmdb.open(file_sentence_lmdb, map_size=int(1e9))

    def get_nns_by_vector(self, emb_vector: List[float], num_nn: int) -> List[Tuple[str, float, str]]:
        """
        Returns a set of nearest neighbour entities for the given embedding vector.
        """
        assert self._annoy_index is not None, "No annoy index has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_entity_mapping is not None, "No annoy entity mapping has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_sentence_mapping is not None, "No annoy sentence mapping has been loaded. Call load_entity_index(file_annoy)"

        nearest_neighbours = self._annoy_index.get_nns_by_vector(emb_vector, num_nn, include_distances=True)

        nns_entities = []
        with self._annoy_entity_mapping.begin() as entity_mapping:
            with self._annoy_sentence_mapping.begin() as sentence_mapping:
                for neighbour_id, distance in zip(nearest_neighbours[0], nearest_neighbours[1]):
                    nns_entities.append((entity_mapping.get(str(neighbour_id).encode()).decode(), distance,
                                         sentence_mapping.get(str(neighbour_id).encode()).decode()))

        return nns_entities

    def get_nns_by_phrase(self, phrase: str, sentence: str, num_nn: int = 1) -> List[Tuple[str, float, str]]:
        """
        Returns a set of nearest neighbour entities for the given phrase.
        """
        assert self._annoy_index is not None, "No annoy index has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_entity_mapping is not None, "No annoy entity mapping has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_sentence_mapping is not None, "No annoy sentence mapping has been loaded. Call load_entity_index(file_annoy)"

        phrase = str(phrase)
        emb, phrase_found = self._get_embedding(phrase, sentence=sentence)
        # Only continue if the query phrase was found in the embedding model, otherwise return an empty list
        if phrase_found:
            return self.get_nns_by_vector(emb, num_nn)
        else:
            return []


class Sent2VecIndexer(AnnoyIndexer):
    def __init__(self, embedding_model_path: str, metric: str ='euclidean', use_compound_splitting: bool=True,
                 compound_splitting_threshold: float=0.5):
        embedding_model = sent2vec.Sent2vecModel()
        embedding_model.load_model(embedding_model_path)
        embedding_vector_size = embedding_model.get_emb_size()

        self._use_compound_splitting = use_compound_splitting
        self._compound_splitting_threshold = compound_splitting_threshold

        super().__init__(embedding_model, embedding_vector_size, metric)

    def _create_entity_index(self, context_data: List[sqlite3.Row]):
        with self._annoy_entity_mapping.begin(write=True) as entity_mapping:
            with self._annoy_sentence_mapping.begin(write=True) as sentence_mapping:
                # Collect all entities for the token based sent2vec model
                entities = set([str(sample['entity_title']) for sample in context_data])

                for sample_id, entity in enumerate(entities):
                    # Replace _ symbols with spaces
                    refactored_entity = entity.replace("_", " ")

                    # Get the entity embedding
                    emb, _ = self._get_embedding(refactored_entity)

                    # Add entity embedding to index
                    self._annoy_index.add_item(sample_id, emb)

                    # Add ID -> word mapping
                    entity_mapping.put(str(sample_id).encode(), entity.encode())
                    # While the sentence mapping is not needed for this model, the code structure needs a dummy.
                    sentence_mapping.put(str(sample_id).encode(), "".encode())

    def _get_embedding(self, phrase: str, sentence: str = "", compound_attempt: bool = False) -> Tuple[List[float],
                                                                                                       bool]:
        emb = self._embedding_model.embed_sentence(phrase)[0]
        phrase_found = True
        if not np.any(emb):
            if self._use_compound_splitting:
                if compound_attempt:
                    log.warning("Phrase '%s' not found in sent2vec. Zero-vector returned." % phrase)
                    phrase_found = False
                else:
                    compound_splitted_phrase = ' '.join(
                        split_compounds(phrase, prop_threshold=self._compound_splitting_threshold))
                    emb, phrase_found = self._get_embedding(compound_splitted_phrase, sentence=sentence,
                                                            compound_attempt=True)
            else:
                log.warning("Phrase '%s' not found in sent2vec. Zero-vector returned." % phrase)
                phrase_found = False

        return emb, phrase_found


class BertIndexer(AnnoyIndexer):
    def __init__(self, bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int=32,
                 layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True, metric: str ='euclidean'):
        be = BertEncoder(bert_config_file=bert_config_file, init_checkpoint=init_checkpoint, vocab_file=vocab_file,
                         seq_len=seq_len, batch_size=batch_size, layer_indexes=layer_indexes,
                         use_one_hot_embeddings=use_one_hot_embeddings, do_lower_case=do_lower_case)

        self._stopwords = set(stopwords.words('german'))
        self._special_mentions_regex = re.compile("^0\\.\\d+$")

        embeddings_vector_size = be.encode(['t'], ['t'])[0][0].shape[-1]
        super().__init__(be, embeddings_vector_size, metric)

    def close_session(self):
        self._embedding_model.close_session()

    def _create_entity_index(self, context_data: List[sqlite3.Row]):
        with self._annoy_entity_mapping.begin(write=True) as entity_mapping:
            with self._annoy_sentence_mapping.begin(write=True) as sentence_mapping:
                context_entities = []
                context_sentences = []
                context_mentions = []

                # Collect all sentences for BERT
                for sample in context_data:
                    context_entities.append(str(sample['entity_title']))
                    context_sentences.append(str(sample['sentence']))
                    context_mentions.append(str(sample['mention']))

                # Get the embeddings for all sentences
                embeddings = self._get_embeddings(context_mentions, context_sentences)

                # Add the embeddings to the annoy index
                for sample_id, data in enumerate(zip(context_data, embeddings)):
                    entity_title = data[0]['entity_title']
                    entity_sentence = data[0]['sentence']
                    emb = data[1]

                    # Add entity embedding to index
                    self._annoy_index.add_item(sample_id, emb)

                    # Add ID -> word mapping
                    entity_mapping.put(str(sample_id).encode(), entity_title.encode())
                    sentence_mapping.put(str(sample_id).encode(), entity_sentence.encode())

    def _get_embeddings(self, phrases: List[str], sentences: List[str]) -> List[np.ndarray]:
        for i in enumerate(phrases):
            phrases[i] = str(phrases[i].strip())

        mentions_embeddings, _ = self._embedding_model.encode(phrases, sentences)
        return mentions_embeddings

    def _get_embedding(self, phrase: str, sentence: str) -> Tuple[np.ndarray, bool]:
        phrase = str(phrase.strip())

        mention_embedding, _ = self._embedding_model.encode([phrase], [sentence])
        return mention_embedding[0], True
