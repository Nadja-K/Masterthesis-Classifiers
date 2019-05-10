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
                 layer_indexes: List[int]=[-1, -2, -3, -4], do_lower_case: bool=True):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        self._output_layer = self._load_model(bert_config_file, init_checkpoint)
        self._sess = tf.Session()
        self._sess.run(tf.global_variables_initializer())

        # And the tokenizer
        # FIXME: handle sentences that are too long (see bert-as-service)
        self._tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)

    def close_session(self):
        self._sess.close()

    def _load_model(self, bert_config_file: str, init_checkpoint: str):
        bert_config = modeling.BertConfig.from_json_file(bert_config_file)
        self.input_ids = tf.placeholder(tf.int32, shape=(None, None), name='input_ids')
        self.input_mask = tf.placeholder(tf.int32, shape=(None, None), name='input_mask')
        self.input_type_ids = tf.placeholder(tf.int32, shape=(None, None), name='input_type_ids')
        use_one_hot_embeddings = False

        # Load the Bert Model
        model = modeling.BertModel(
            config=bert_config,
            is_training=False,
            input_ids=self.input_ids,
            input_mask=self.input_mask,
            token_type_ids=self.input_type_ids,
            use_one_hot_embeddings=use_one_hot_embeddings
        )
        tvars = tf.trainable_variables()

        # Load the checkpoint
        (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                   init_checkpoint)
        tf.train.init_from_checkpoint(self.init_checkpoint, assignment_map)

        # Get the output layer of the model
        return model.get_sequence_output()

    def encode_sentence(self, sentence: str):
        # FIXME
        pass

    def encode_sentences(self, sentences: List[str]):
        all_token_embeddings = []
        all_feature_tokens = []
        # FIXME: do it all at once / batches? Instead of one by one
        for feature in convert_lst_to_features(sentences, max_seq_length=self.seq_len, tokenizer=self.tokenizer):
            sample = {
                self.input_ids: [feature.input_ids],
                self.input_mask: [feature.input_mask],
                self.input_type_ids: [feature.input_type_ids]
            }
            token_embeddings = self.sess.run(self.output_layer, feed_dict=sample)
            # print(feature.tokens)
            # print(token_embeddings.shape)
            # print(token_embeddings)
            #
            all_token_embeddings.append(token_embeddings[0])
            all_feature_tokens.append(feature.tokens)

        return all_token_embeddings, all_feature_tokens
