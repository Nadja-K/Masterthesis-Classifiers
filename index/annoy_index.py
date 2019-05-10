import sqlite3

import annoy
import lmdb
import sent2vec
import logging
import numpy as np
import nltk
import time
import os
import glob
import re

from nltk.corpus import stopwords
from pathlib import Path
from typing import Set, List, Tuple, Union
from abc import ABCMeta, abstractmethod
from utils.utils import split_compounds
from bert.bert import BertEncoder

log = logging.getLogger(__name__)


class AnnoyIndexer(metaclass=ABCMeta):
    def __init__(self, embedding_model, embedding_vector_size, metric):
        self._annoy_index = None
        self._annoy_mapping = None
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
        file_lmdb = output_filename + "_" + timestamp + ".lmdb"

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
        self._annoy_index.save(file_annoy)

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

    def get_nns_by_phrase(self, phrase: str, sentence: str, num_nn: int = 1) -> List[Tuple[str, float]]:
        """
        Returns a set of nearest neighbour entities for the given phrase.
        """
        assert self._annoy_index is not None, "No annoy index has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_mapping is not None, "No annoy mapping has been loaded. Call load_entity_index(file_annoy)"

        phrase = str(phrase)
        refactored_phrase = phrase.replace("_", " ")
        emb, phrase_found = self._get_embedding(refactored_phrase, sentence=sentence)
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
        with self._annoy_mapping.begin(write=True) as mapping:
            # Collect all entities for the token based sent2vec model
            entities = set([str(sample['entity_title']) for sample in context_data])

            for sample_id, entity in enumerate(entities):
                # Replace _ symbols with spaces
                refactored_entity = entity.replace("_", " ")

                # Get the entity embedding
                emb, _ = self._get_embedding(refactored_entity)

                # Add entity embedding to index
                # log.info("add item | %s | %s" % (sample_id, refactored_entity))
                self._annoy_index.add_item(sample_id, emb)

                # Add ID -> word mapping
                mapping.put(str(sample_id).encode(), entity.encode())

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

    def _get_embedding(self, phrase: str, sentence: str = "", compound_attempt: bool = False) -> Tuple[List[float], bool]:
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

        # self._word_tokenizer = nltk.tokenize.WordPunctTokenizer()
        self._stopwords = set(stopwords.words('german'))

        embeddings_vector_size = be.encode([['t']], is_tokenized=True)[0][0].shape[-1]
        super().__init__(be, embeddings_vector_size, metric)

    def close_session(self):
        self._embedding_model.close_session()

    def _create_entity_index(self, context_data: List[sqlite3.Row]):
        with self._annoy_mapping.begin(write=True) as mapping:
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
                emb = data[1]

                # Add entity embedding to index
                # log.info("add item | %s | %s | %s" % (sample_id, entity_title, emb.shape))
                self._annoy_index.add_item(sample_id, emb)

                # Add ID -> word mapping
                mapping.put(str(sample_id).encode(), entity_title.encode())

    # FIXME: remove this
    # @staticmethod
    # def _find_sub_list(pattern: List[str], sentence: List[str]):
    #     sll = len(pattern)
    #     for ind in (i for i, e in enumerate(sentence) if pattern[0] in e):
    #         if pattern[0] in sentence[ind] and pattern[-1] in sentence[ind+sll- 1] and sentence[ind+1: ind+sll-1] == pattern[1:-1]:
    #             return ind, ind+sll-1
    #
    #     return -1, -1

    def _get_avg_phrase_embedding(self, phrase: str, sentence: str, token_embeddings: np.ndarray,
                                  token_mapping: List) -> np.ndarray:
        # Find the start position of the phrase in the sentence
        phrase_start_index = re.search(r'((?<=[^\\w])|(^))(' + re.escape(phrase) + ')(?![\\w])', sentence)
        # If the strict regex didn't find the phrase, use a more lenient regex
        if phrase_start_index is None:
            phrase_start_index = re.search(r'(' + re.escape(phrase) + ')', sentence)
            print(phrase, sentence)
        phrase_start_index = phrase_start_index.start()

        # Now the start position without counting spaces
        phrase_start_index = phrase_start_index - sentence[:phrase_start_index].count(" ")
        # Get the end position as well (without counting spaces)
        phrase_end_index = phrase_start_index + len(phrase.replace(" ", "")) - 1

        string_position = 0
        phrase_start_token_index = -1
        phrase_end_token_index = -1
        for current_token, next_token in zip(token_mapping[1:-1], token_mapping[2:-1]):
            cur_word_token, cur_word_token_emb_index = current_token
            next_word_token, next_word_token_emb_index = next_token

            for _ in cur_word_token:
                if string_position == phrase_start_index:
                    phrase_start_token_index = cur_word_token_emb_index

                if string_position == phrase_end_index:
                    phrase_end_token_index = next_word_token_emb_index
                    break

                string_position += 1
        # if is_tokenized:
        #     tokenized_phrase = self._word_tokenizer.tokenize(phrase)
        #     phrase_start_token_index, phrase_end_token_index = self._find_sub_list(tokenized_phrase, sentence)
        #     assert phrase_end_token_index != -1 and phrase_start_token_index != -1
        #
        #     phrase_start_token_index += 1
        #     phrase_end_token_index += 1
        # else:
        #     # It is possible that there are still leading or trailing spaces in the phrase that might cause problems
        #     phrase = str(phrase.strip())
        #
        #     # Find the start position of the phrase in the sentence
        #     phrase_start_index = re.search(r'((?<=[^\\w])|(^))(' + re.escape(phrase) + ')(?![\\w])', sentence)
        #     # If the strict regex didn't find the phrase, use a more lenient regex
        #     if phrase_start_index is None:
        #         phrase_start_index = re.search(r'(' + re.escape(phrase) + ')', sentence)
        #         print(phrase, sentence)
        #     phrase_start_index = phrase_start_index.start()
        #
        #     # Now the start position without counting spaces
        #     phrase_start_index = phrase_start_index - sentence[:phrase_start_index].count(" ")
        #     # Get the end position as well (without counting spaces)
        #     phrase_end_index = phrase_start_index + len(phrase.replace(" ", ""))
        #
        #     # print(phrase, sentence)
        #     string_position = 0
        #     phrase_start_token_index = -1
        #     phrase_end_token_index = -1
        #     # Get the index of the corresponding tokens for the phrase
        #     for token_index, token in enumerate(tokens[1:-1]):
        #         if phrase_start_index <= string_position < phrase_end_index:
        #             if string_position == phrase_start_index:
        #                 phrase_start_token_index = token_index + 1
        #             else:
        #                 phrase_end_token_index = token_index + 1
        #             # print(token_index + 1, token, string_position)
        #
        #         if token == '[UNK]':
        #             string_position += 1
        #         else:
        #             string_position += len(token.replace("##", ""))

        # Calculate the average of all token embeddings that belong to the phrase
        # avg_phrase_embedding = np.mean(token_embeddings[phrase_start_token_index:phrase_end_token_index + 1], axis=0)
        avg_phrase_embedding = np.mean(token_embeddings[phrase_start_token_index:phrase_end_token_index], axis=0)
        return avg_phrase_embedding

    def _get_embeddings(self, phrases: List[str], sentences: List[str]) -> List[np.ndarray]:
        tokenized_sentences = []
        mappings = []
        for sentence in sentences:
            # FIXME: move tokenizer out of embedding model and move it into this class
            # FIXME: remove is_tokenized from all methods because the tokenization NEEDS to be done with a custom version of the tokenizer anyway
            tokens, mapping = self._embedding_model._tokenizer.tokenize(sentence)
            # Update the mapping with the CLS and SEP tag
            mapping = [('[CLS]', 0)] + [(token, token_index+1) for (token, token_index) in mapping] + [('[SEP]', mapping[-1][1]+2)]

            tokenized_sentences.append(tokens)
            mappings.append(mapping)
        #
        # sentences = tokenized_sentences
        sentences_embeddings, _ = self._embedding_model.encode(tokenized_sentences, is_tokenized=True)
        # sentences_embeddings, sentences_tokens = self._embedding_model.encode(sentences)

        phrase_embeddings = []
        for sentence_data in zip(phrases, sentences, sentences_embeddings, mappings):
            # FIXME: handle max_seq_len=256 cases
            phrase, sentence, tokens_embs, mapping = sentence_data
            # phrase_emb = self._get_avg_phrase_embedding(phrase, sentence, sentence_emb, sentence_tok, is_tokenized=True)
            phrase_emb = self._get_avg_phrase_embedding(phrase, sentence, token_embeddings=tokens_embs, token_mapping=mapping)
            phrase_embeddings.append(phrase_emb)

        return phrase_embeddings

    def _get_embedding(self, phrase: str, sentence: str) -> Tuple[np.ndarray, bool]:
        tokens, mapping = self._embedding_model._tokenizer.tokenize(sentence)
        tokens_embs, new_tokens = self._embedding_model.encode([tokens], is_tokenized=True)

        # Update the mapping with the CLS and SEP tag
        mapping = [('[CLS]', 0)] + [(token, token_index+1) for (token, token_index) in mapping] + [('[SEP]', mapping[-1][1]+2)]

        # FIXME: handle max_seq_len=256 cases
        # sentence_embs, sentence_tokens = self._embedding_model.encode([sentence])
        # phrase_emb = self._get_avg_phrase_embedding(phrase, sentence, sentence_embs[0], sentence_tokens[0], is_tokenized=True)
        phrase_emb = self._get_avg_phrase_embedding(phrase, sentence, token_embeddings=tokens_embs[0], token_mapping=mapping)
        return phrase_emb, True
