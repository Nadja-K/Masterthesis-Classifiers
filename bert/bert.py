# Based on the code found in:
# https://github.com/danielkaifeng/TF_BERT_Chinese_Article_Auto_Generation/blob/911d31b7b49fa653a80d6bc501ea41cd676d6428/run_classifier.py
# https://github.com/hanxiao/bert-as-service/blob/7c2fec7b0322cfeed6a22db560266f3d87d94d2e/server/bert_serving/server/graph.py

from bert import modeling
from bert import tokenization
from bert.extract_features import convert_lst_to_features

import logging
import tensorflow as tf
import re
import numpy as np
from typing import List, Union, Tuple

log = logging.getLogger(__name__)


class BertEncoder:
    def __init__(self, bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int=32,
                 layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True, load_model: bool=True):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        if load_model:
            bert_config = modeling.BertConfig.from_json_file(bert_config_file)
            self._input_ids = tf.placeholder(tf.int32, shape=(None, None), name='input_ids')
            self._input_mask = tf.placeholder(tf.int32, shape=(None, None), name='input_mask')
            self._input_type_ids = tf.placeholder(tf.int32, shape=(None, None), name='input_type_ids')
            self._mention_mask = tf.placeholder(tf.float32, shape=(None, None), name='mention_mask')

            self._output_layer = self.load_model(bert_config=bert_config, init_checkpoint=init_checkpoint,
                                                 layer_indexes=layer_indexes, input_ids=self._input_ids,
                                                 input_mask=self._input_mask, input_type_ids=self._input_type_ids,
                                                 mention_mask=self._mention_mask, is_training=False,
                                                 use_one_hot_embeddings=use_one_hot_embeddings)

        # FIXME: make this an option in the remote_config
        gpu_memory_fraction = 1.0
        self._sess_config = tf.ConfigProto()
        self._sess_config.gpu_options.allow_growth = True
        self._sess_config.gpu_options.per_process_gpu_memory_fraction = gpu_memory_fraction
        self._sess_config.log_device_placement = False
        self._sess = None
        self.open_session()

        # And the tokenizer
        self._tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)

    def open_session(self):
        if self._sess is not None:
            self.close_session()
        self._sess = tf.Session(config=self._sess_config)
        self._sess.run(tf.global_variables_initializer())

    def close_session(self):
        self._sess.close()

    @staticmethod
    def load_model(bert_config, init_checkpoint: Union[str, None], layer_indexes: List[int], input_ids, input_mask, input_type_ids,
                   mention_mask, is_training: bool=False, use_one_hot_embeddings: bool=False, scope: str=None):
        # Load the Bert Model
        model = modeling.BertModel(
            config=bert_config,
            is_training=is_training,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=input_type_ids,
            use_one_hot_embeddings=use_one_hot_embeddings,
            scope=scope
        )
        tvars = tf.trainable_variables()
        initialized_variable_names = {}

        # Load the checkpoint
        if init_checkpoint is None:
            tf.logging.info("No checkpoint was loaded.")
        else:
            (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                       init_checkpoint)
            tf.train.init_from_checkpoint(init_checkpoint, assignment_map)

        # Get the defined output layer of the model (or concat multiple layers if specified)
        if len(layer_indexes) == 1:
            output_layer = model.get_all_encoder_layers()[layer_indexes[0]]
        else:
            all_layers = [model.get_all_encoder_layers()[l] for l in layer_indexes]
            output_layer = tf.concat(all_layers, -1)

        # Just some prints to make sure the ckpt init worked
        if init_checkpoint is not None:
            tf.logging.info("*** Trainable Variables ***")
            for var in tvars:
                init_string = ""
                if var.name in initialized_variable_names:
                    init_string = ", *INIT_FROM_CKPT*"
                tf.logging.info("   name = %s, shape = %s%s", var.name, var.shape, init_string)

        mention_embedding_layer = tf.div(tf.reduce_sum(output_layer * tf.expand_dims(mention_mask, -1), axis=1),
                                         tf.expand_dims(tf.reduce_sum(mention_mask, axis=1), axis=-1))

        return mention_embedding_layer

    @staticmethod
    def _check_length(texts: Union[List[str], List[List[str]]], len_limit: int, tokenized: bool):
        """
        Based on the code found in: https://github.com/hanxiao/bert-as-service
        """
        if tokenized:
            # texts is already tokenized as list of str
            return all(len(t) <= len_limit for t in texts)
        else:
            # do a simple whitespace tokenizer
            return all(len(t.split()) <= len_limit for t in texts)

    @staticmethod
    def _check_input_lst_lst_str(texts: List[List[str]]):
        """
        Based on the code found in: https://github.com/hanxiao/bert-as-service
        """
        if not isinstance(texts, list):
            raise TypeError('"texts" must be %s, but received %s' % (type([]), type(texts)))
        if not len(texts):
            raise ValueError(
                '"texts" must be a non-empty list, but received %s with %d elements' % (type(texts), len(texts)))
        for s in texts:
            BertEncoder._check_input_lst_str(s)

    @staticmethod
    def _check_input_lst_str(texts: List[str]):
        """
        Based on the code found in: https://github.com/hanxiao/bert-as-service
        """
        if not isinstance(texts, list):
            raise TypeError('"%s" must be %s, but received %s' % (texts, type([]), type(texts)))
        if not len(texts):
            raise ValueError(
                '"%s" must be a non-empty list, but received %s with %d elements' % (texts, type(texts), len(texts)))
        for idx, s in enumerate(texts):
            if not isinstance(s, str):
                raise TypeError('all elements in the list must be %s, but element %d is %s' % (type(''), idx, type(s)))
            if not s.strip():
                raise ValueError(
                    'all elements in the list must be non-empty string, but element %d is %s' % (idx, repr(s)))

    def tokenize(self, sentence: str) -> Tuple[List[str], List[Tuple[str, int]]]:
        tokens, mapping = self._tokenizer.tokenize(sentence)
        return tokens, mapping

    def clean_text(self, text: str) -> str:
        return self._tokenizer.clean_text(text)

    def _get_mention_mask(self, mention: str, sentence: str, token_mapping: List[Tuple[str, int]]) -> np.ndarray:
        mention = self.clean_text(mention)
        sentence = self.clean_text(sentence)
        mask = np.zeros(self._seq_len)

        # Find the start position of the phrase in the sentence
        phrase_start_index = re.search(r'((?<=[^\\w])|(^))(' + re.escape(mention) + ')(?![\\w])', sentence)

        # If the strict regex didn't find the phrase, use a more lenient regex
        if phrase_start_index is None:
            phrase_start_index = re.search(r'(' + re.escape(mention) + ')', sentence)

        phrase_start_index = phrase_start_index.start()

        # Now the start position without counting spaces
        phrase_start_index = phrase_start_index - sentence[:phrase_start_index].count(" ")
        # Get the end position as well (without counting spaces)
        phrase_end_index = phrase_start_index + len(mention.replace(" ", "")) - 1

        string_position = 0
        phrase_start_token_index = -1
        phrase_end_token_index = -1
        for current_token, next_token in zip(token_mapping[1:-1], token_mapping[2:]):
            cur_word_token, cur_word_token_emb_index = current_token
            next_word_token, next_word_token_emb_index = next_token

            # If the end has already been found, stop
            if phrase_end_token_index != -1:
                break

            for t in cur_word_token:
                if string_position == phrase_start_index:
                    phrase_start_token_index = cur_word_token_emb_index

                if string_position == phrase_end_index:
                    phrase_end_token_index = next_word_token_emb_index
                    break

                string_position += 1

        if (phrase_start_token_index >= self._seq_len or phrase_end_token_index >= self._seq_len):
            log.warning("The current sample has more tokens than max_seq_len=%d allows and the mention seems "
                        "to be out of the boundaries in this case. Instead of an avg. phrase embedding, an avg. "
                        "sentence embedding will be returned.\n"
                        "Sentence: %s\n"
                        "Phrase: %s" % (self._seq_len, sentence, mention))
            mask = np.ones(self._seq_len)
        else:
            assert len(mask[phrase_start_token_index:phrase_end_token_index]) > 0, \
                "Something went wrong with the phrase embedding retrieval."

            mask[phrase_start_token_index:phrase_end_token_index] = 1

        return mask

    def encode(self, mentions: List[str], original_sentences: List[str]):
        # Tokenize the sentences
        tokenized_sentences = []
        tokens_mappings = []
        for sentence in original_sentences:
            tokens, mapping = self.tokenize(sentence)

            # Update the mapping with the CLS and SEP tag
            mapping = [('[CLS]', 0)] + [(token, token_index+1) for (token, token_index) in
                                        mapping] + [('[SEP]', mapping[-1][1]+2)]
            tokenized_sentences.append(tokens)
            tokens_mappings.append(mapping)

        # Check if the tokenized input format is correct
        self._check_input_lst_lst_str(tokenized_sentences)

        # Check if all sentences are shorter than the max seq len
        if not self._check_length(tokenized_sentences, self._seq_len, True):
            log.warning('Some of your sentences have more tokens than "max_seq_len=%d" set,'
                        'as a consequence you may get less-accurate or truncated embeddings or lose the '
                        'embedding for a specified phrase of a sentence.\n' % self._seq_len)

        all_mention_embeddings = []
        all_feature_tokens = []

        batch = {
            self._input_ids: [],
            self._input_mask: [],
            self._input_type_ids: [],
            self._mention_mask: []
        }
        # Tokenizer is still needed for mapping and some other stuff that happens in the convert method
        for sample_index, data in enumerate(zip(convert_lst_to_features(tokenized_sentences,
                                                                        max_seq_length=self._seq_len,
                                                                        tokenizer=self._tokenizer),
                                                mentions, original_sentences, tokens_mappings)):
            feature, mention, sentence, token_mapping = data

            # Create mention mask
            mention_mask = self._get_mention_mask(mention, sentence, token_mapping)

            batch[self._input_ids].append(feature.input_ids)
            batch[self._input_mask].append(feature.input_mask)
            batch[self._input_type_ids].append(feature.input_type_ids)
            batch[self._mention_mask].append(mention_mask)
            # log.info("Sample: %d | Tokens: %s" % (sample_index, feature.tokens))

            all_feature_tokens.append(feature.tokens)
            if sample_index % self._batch_size == 0:
                batch_token_embeddings = self._sess.run(self._output_layer, feed_dict=batch)

                for token_embeddings in batch_token_embeddings:
                    all_mention_embeddings.append(token_embeddings)

                # Reset the batch
                batch = {
                    self._input_ids: [],
                    self._input_mask: [],
                    self._input_type_ids: [],
                    self._mention_mask: []
                }

        # Handle leftover samples that did not fit in the last batch
        if len(batch[self._input_ids]) > 0:
            batch_mention_embeddings = self._sess.run(self._output_layer, feed_dict=batch)

            for mention_embedding in batch_mention_embeddings:
                all_mention_embeddings.append(mention_embedding)

        return all_mention_embeddings, all_feature_tokens
