import sqlite3

import annoy
import lmdb
import sent2vec
import logging
import numpy as np
import nltk
import time

from pathlib import Path
from typing import Set, List, Tuple
from abc import ABCMeta, abstractmethod
from utils.utils import split_compounds
from bert_serving.client import BertClient

log = logging.getLogger(__name__)


class AnnoyIndexer(metaclass=ABCMeta):
    def __init__(self, embedding_model, embedding_vector_size, metric):
        self._annoy_index = None
        self._annoy_mapping = None
        self._metric = metric

        self._embedding_model = embedding_model
        self._embedding_vector_size = embedding_vector_size

    @abstractmethod
    def _get_embedding(self, phrase: str) -> Tuple[List[float], bool]:
        pass

    @abstractmethod
    def _create_entity_index(self, context_data: List[sqlite3.Row]):
        with self._annoy_mapping.begin(write=True) as mapping:
            context_entities = {}

            # Collect all entities
            for sample in context_data:
                context_entities[str(sample['entity_title'])] = int(sample['entity_id'])

            for entity, entity_id in context_entities.items():
                # Replace _ symbols with spaces
                refactored_entity = entity.replace("_", " ")

                # Get the entity embedding
                emb, _ = self._get_embedding(refactored_entity)

                # Add entity embedding to index
                self._annoy_index.add_item(entity_id, emb)

                # Add ID <-> word mapping
                mapping.put(str(entity_id).encode(), entity.encode())

    def create_entity_index(self, context_data: List[sqlite3.Row], output_filename: str, num_trees: int=30):
        """
        The public create entity index method that users can call.
        The basic structure is the same but the entity embedding collection is different for every embedding model
        and has to be implemented explicitly using the private _create_entity_index method.
        """
        file_annoy = output_filename + ".ann"
        file_lmdb = output_filename + ".lmdb"

        # Create AnnoyIndex instance
        self._annoy_index = annoy.AnnoyIndex(self._embedding_vector_size, metric=self._metric)

        # Create mapping instance
        self._annoy_mapping = lmdb.open(file_lmdb, map_size=int(1e9))

        # Retrieve entity embeddings and add them to the annoy index
        self._create_entity_index(context_data)

        # Build annoy index
        log.info("Building annoy index now.")
        start = time.time()
        self._annoy_index.build(num_trees)
        log.info("Building annoy index took %s" % (time.time() - start))

        # Save annoy index
        # FIXME: make this optional? Because it cant be loaded anyway if the filesize is >2GB
        # self._annoy_index.save(file_annoy)

    def load_entity_index(self, file_annoy: str):
        """
        Load an annoy index and the corresponding lmdb mapping.

        :param file_annoy: 'path/filename.ann'
        """
        file_lmdb = ".".join(file_annoy.split(".")[:-1]) + ".lmdb"
        assert Path(file_annoy).is_file(), "The annoy file could not be found. Make sure the path is correct."
        assert Path(file_lmdb).is_dir(), "The lmdb mapping could not be found. Make sure it is in the same " \
                                          "directory as the .ann file and has the same file name except for " \
                                          "the file extension (.lmdb)."

        self._annoy_index = annoy.AnnoyIndex(self._embedding_vector_size, metric=self._metric)
        self._annoy_index.load(file_annoy)

        self._annoy_mapping = lmdb.open(file_lmdb, map_size=int(1e9))

    def get_nns_by_vector(self, emb_vector: List[float], num_nn: int) -> List[Tuple[str, float]]:
        """
        Returns a set of nearest neighbour entities for the given embedding vector.
        """
        assert self._annoy_index is not None, "No annoy index has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_mapping is not None, "No annoy mapping has been loaded. Call load_entity_index(file_annoy)"

        nearest_neighbours = self._annoy_index.get_nns_by_vector(emb_vector, num_nn, include_distances=True)

        nns_entities = []
        with self._annoy_mapping.begin() as mapping:
            for neighbour_id, distance in zip(nearest_neighbours[0], nearest_neighbours[1]):
                nns_entities.append((mapping.get(str(neighbour_id).encode()).decode(), distance))

        return nns_entities

    def get_nns_by_phrase(self, phrase: str, num_nn: int) -> List[Tuple[str, float]]:
        """
        Returns a set of nearest neighbour entities for the given phrase.
        """
        assert self._annoy_index is not None, "No annoy index has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_mapping is not None, "No annoy mapping has been loaded. Call load_entity_index(file_annoy)"

        phrase = str(phrase)
        refactored_phrase = phrase.replace("_", " ")

        emb, phrase_found = self._get_embedding(refactored_phrase)
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
        super()._create_entity_index(context_data)

    # FIXME: remove this or make a sent2vec classifier that does not work on token level
    # def _create_entity_index(self, context_data: List[sqlite3.Row]):
    #     """
    #     Sent2Vec test for using context sentences as entity reference instead of working on token level.
    #
    #     """
    #     with self._annoy_mapping.begin(write=True) as mapping:
    #         context_entities = []
    #         context_sentences = []
    #
    #         # Collect all sentences for BERT
    #         for sample in context_data:
    #             context_entities.append(
    #                 {'entity_id': int(sample['entity_id']), 'entity_title': str(sample['entity_title'])})
    #             context_sentences.append(str(sample['sentence']))
    #             # context_sentences.append(self._word_tokenizer.tokenize(str(sample['sentence'])))
    #
    #         # Get the embeddings for all sentences
    #         embeddings = self._embedding_model.embed_sentences(context_sentences)
    #
    #         # Add the embeddings to the annoy index
    #         for data in zip(context_entities, embeddings):
    #             entity_id = data[0]['entity_id']
    #             entity_title = data[0]['entity_title']
    #             emb = data[1]
    #
    #             # Add entity embedding to index
    #             self._annoy_index.add_item(entity_id, emb)
    #
    #             # Add ID <-> word mapping
    #             mapping.put(str(entity_id).encode(), entity_title.encode())

    def _get_embedding(self, phrase: str, compound_attempt=False) -> Tuple[List[float], bool]:
        emb = self._embedding_model.embed_sentence(phrase)[0]
        phrase_found = True
        if not np.any(emb):
            if self._use_compound_splitting:
                if compound_attempt:
                    log.warning("Phrase '%s' not found in sent2vec. Zero-vector returned." % phrase)
                    phrase_found = False
                else:
                    # log.warning("Phrase '%s' not found in sent2vec. Attempting again with compound splitting." % phrase)
                    compound_splitted_phrase = ' '.join(
                        split_compounds(phrase, prop_threshold=self._compound_splitting_threshold))
                    emb, phrase_found = self._get_embedding(compound_splitted_phrase, True)
            else:
                log.warning("Phrase '%s' not found in sent2vec. Zero-vector returned." % phrase)
                phrase_found = False

        return emb, phrase_found


class BertIndexer(AnnoyIndexer):
    def __init__(self, bert_service_ip: str, bert_service_port: int, bert_service_port_out: int,
                 metric: str ='euclidean'):
        bc = BertClient(ip=bert_service_ip, port=bert_service_port, port_out=bert_service_port_out)
        embedding_vector_size = bc.encode(['test']).flatten().shape[0]

        self._word_tokenizer = nltk.tokenize.WordPunctTokenizer()
        super().__init__(bc, embedding_vector_size, metric)

    def _create_entity_index(self, context_data: List[sqlite3.Row]):
        with self._annoy_mapping.begin(write=True) as mapping:
            context_entities = []
            context_sentences = []

            # Collect all sentences for BERT
            for sample in context_data:
                context_entities.append({'entity_id': int(sample['entity_id']), 'entity_title': str(sample['entity_title'])})
                context_sentences.append(str(sample['sentence']))
                # context_sentences.append(self._word_tokenizer.tokenize(str(sample['sentence'])))

            # Get the embeddings for all sentences
            embeddings = self._get_embeddings(context_sentences)

            # Add the embeddings to the annoy index
            for data in zip(context_entities, embeddings):
                entity_id = data[0]['entity_id']
                entity_title = data[0]['entity_title']
                emb = data[1]

                # Add entity embedding to index
                self._annoy_index.add_item(entity_id, emb)

                # Add ID <-> word mapping
                mapping.put(str(entity_id).encode(), entity_title.encode())

    def _get_embeddings(self, sentences: List[str]) -> Tuple[List[float]]:
        # return self._embedding_model.encode(sentences, is_tokenized=True)
        return self._embedding_model.encode(sentences)

    def _get_embedding(self, phrase: str) -> Tuple[List[float], bool]:
        # phrase = self._word_tokenizer.tokenize(phrase)
        # return self._embedding_model.encode([phrase], is_tokenized=True)[0], True
        return self._embedding_model.encode([phrase])[0], True
