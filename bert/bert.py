# Based on the code found in:
# https://github.com/danielkaifeng/TF_BERT_Chinese_Article_Auto_Generation/blob/911d31b7b49fa653a80d6bc501ea41cd676d6428/run_classifier.py
# https://github.com/hanxiao/bert-as-service/blob/7c2fec7b0322cfeed6a22db560266f3d87d94d2e/server/bert_serving/server/graph.py

from bert import modeling
from bert import tokenization
from bert.extract_features import convert_lst_to_features

import logging
import tensorflow as tf
from typing import List, Union

log = logging.getLogger(__name__)

class BertEncoder:
    def __init__(self, bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int=32,
                 layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        self._output_layer = self._load_model(bert_config_file, init_checkpoint, use_one_hot_embeddings)

        # FIXME: make this an option in the remote_config
        gpu_memory_fraction = 0.7
        sess_config = tf.ConfigProto()
        sess_config.gpu_options.allow_growth = True
        sess_config.gpu_options.per_process_gpu_memory_fraction = gpu_memory_fraction
        sess_config.log_device_placement = False
        self._sess = tf.Session(config=sess_config)
        self._sess.run(tf.global_variables_initializer())

        # And the tokenizer
        # FIXME: handle sentences that are too long (see bert-as-service)
        self._tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)

    def close_session(self):
        self._sess.close()

    def _load_model(self, bert_config_file: str, init_checkpoint: str, use_one_hot_embeddings: bool=False):
        bert_config = modeling.BertConfig.from_json_file(bert_config_file)
        self._input_ids = tf.placeholder(tf.int32, shape=(None, None), name='input_ids')
        self._input_mask = tf.placeholder(tf.int32, shape=(None, None), name='input_mask')
        self._input_type_ids = tf.placeholder(tf.int32, shape=(None, None), name='input_type_ids')

        # Load the Bert Model
        model = modeling.BertModel(
            config=bert_config,
            is_training=False,
            input_ids=self._input_ids,
            input_mask=self._input_mask,
            token_type_ids=self._input_type_ids,
            use_one_hot_embeddings=use_one_hot_embeddings
        )
        tvars = tf.trainable_variables()

        # Load the checkpoint
        (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                   init_checkpoint)
        tf.train.init_from_checkpoint(init_checkpoint, assignment_map)

        # Get the defined output layer of the model (or concat multiple layers if specified)
        if len(self._layer_indexes) == 1:
            return model.get_all_encoder_layers()[self._layer_indexes[0]]
        else:
            all_layers = [model.get_all_encoder_layers()[l] for l in self._layer_indexes]
            return tf.concat(all_layers, -1)

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

    def encode(self, sentences: Union[List[List[str]], List[str]], is_tokenized: bool=True):
        # FIXME: remove the tokenized stuff, just check that the stuff is tokenized bc thats what I need here with my custom tokenizer anyway
        # Check if the input format is correct
        if is_tokenized:
            self._check_input_lst_lst_str(sentences)
        else:
            self._check_input_lst_str(sentences)

        # Check if all sentences are shorter than the max seq len
        if not self._check_length(sentences, self._seq_len, is_tokenized):
            log.warning('Some of your sentences have more tokens than "max_seq_len=%d" set,'
                        'as a consequence you may get less-accurate or truncated embeddings or lose the '
                        'embedding for a specified phrase of a sentence.\n')

        all_token_embeddings = []
        all_feature_tokens = []

        batch = {
            self._input_ids: [],
            self._input_mask: [],
            self._input_type_ids: []
        }
        for sample_index, feature in enumerate(convert_lst_to_features(sentences,
                                                                       max_seq_length=self._seq_len,
                                                                       tokenizer=self._tokenizer,
                                                                       is_tokenized=is_tokenized)):
            batch[self._input_ids].append(feature.input_ids)
            batch[self._input_mask].append(feature.input_mask)
            batch[self._input_type_ids].append(feature.input_type_ids)

            all_feature_tokens.append(feature.tokens)
            if sample_index % self._batch_size == 0:
                batch_toke_embeddings = self._sess.run(self._output_layer, feed_dict=batch)

                for token_embeddings in batch_toke_embeddings:
                    all_token_embeddings.append(token_embeddings)

                # Reset the batch
                batch = {
                    self._input_ids: [],
                    self._input_mask: [],
                    self._input_type_ids: []
                }

        # Handle leftover samples that did not fit in the last batch
        if len(batch[self._input_ids]) > 0:
            batch_token_embeddings = self._sess.run(self._output_layer, feed_dict=batch)

            for token_embeddings in batch_token_embeddings:
                all_token_embeddings.append(token_embeddings)

        return all_token_embeddings, all_feature_tokens
