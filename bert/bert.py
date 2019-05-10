# Based on the code found in:
# https://github.com/danielkaifeng/TF_BERT_Chinese_Article_Auto_Generation/blob/911d31b7b49fa653a80d6bc501ea41cd676d6428/run_classifier.py
# https://github.com/hanxiao/bert-as-service/blob/7c2fec7b0322cfeed6a22db560266f3d87d94d2e/server/bert_serving/server/graph.py

from bert import modeling
from bert import tokenization
from bert.extract_features import convert_lst_to_features

import tensorflow as tf
from typing import List


class BertEncoder:
    def __init__(self, bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int=32,
                 layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        self._output_layer = self._load_model(bert_config_file, init_checkpoint, use_one_hot_embeddings)
        self._sess = tf.Session()
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

        # Get the output layer of the model
        # FIXME: make the layer a param that can be set (maybe even concat somehow?)
        return model.get_all_encoder_layers()[-2]

    def encode(self, sentences: List[str]):
        all_token_embeddings = []
        all_feature_tokens = []

        batch = {
            self._input_ids: [],
            self._input_mask: [],
            self._input_type_ids: []
        }
        for sample_index, feature in enumerate(convert_lst_to_features(
                sentences, max_seq_length=self._seq_len, tokenizer=self._tokenizer)):
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
            batch_toke_embeddings = self._sess.run(self._output_layer, feed_dict=batch)

            for token_embeddings in batch_toke_embeddings:
                all_token_embeddings.append(token_embeddings)

        return all_token_embeddings, all_feature_tokens
