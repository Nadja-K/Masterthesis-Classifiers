# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Based on the code found in:
# https://github.com/hanxiao/bert-as-service/blob/master/server/bert_serving/server/bert/extract_features.py

"""Extract pre-computed feature vectors from BERT."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from typing import List, Union
from bert import tokenization
import tensorflow as tf


class InputExample(object):
    def __init__(self, unique_id: int, text_a: Union[List[str], str], text_b: Union[List[str], str]):
        self.unique_id = unique_id
        self.text_a = text_a
        self.text_b = text_b


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, unique_id: int, tokens: List[str], input_ids: List[int], input_mask: List[int],
                 input_type_ids: List[int]):
        self.unique_id = unique_id
        self.tokens = tokens
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.input_type_ids = input_type_ids


# FIXME: remove eventually
# def input_fn_builder(sentences: List[str], tokenizer: tokenization.FullTokenizer, max_seq_length: int):
#     unique_id_to_feature = {}
#
#     def gen():
#         for feature in convert_lst_to_features(sentences, max_seq_length=max_seq_length, tokenizer=tokenizer):
#             unique_id_to_feature[feature.unique_id] = feature
#             yield {
#                 'unique_ids': [feature.unique_id],
#                 'input_ids': [feature.input_ids],
#                 'input_mask': [feature.input_mask],
#                 'input_type_ids': [feature.input_type_ids]
#             }
#
#     def input_fn(params):
#         """The actual input function."""
#         # batch_size = params["batch_size"]
#
#         return (tf.data.Dataset.from_generator(
#             gen,
#             output_types={
#                 'unique_ids': tf.int32,
#                 'input_ids': tf.int32,
#                 'input_mask': tf.int32,
#                 'input_type_ids': tf.int32
#             },
#             output_shapes={
#                 'unique_ids': (None,),
#                 'input_ids': (None, None),
#                 'input_mask': (None, None),
#                 'input_type_ids': (None, None)
#             }
#         ))
#
#     return input_fn, unique_id_to_feature


# FIXME: remove eventually
# def model_fn_builder(bert_config, init_checkpoint, layer_indexes, use_one_hot_embeddings):
#     """Returns `model_fn` closure for TPUEstimator."""
#
#     def model_fn(features, labels, mode, params):  # pylint: disable=unused-argument
#         """The `model_fn` for TPUEstimator."""
#
#         with tf.device("/device:GPU:2"):
#             unique_ids = features["unique_ids"]
#             input_ids = features["input_ids"]
#             input_mask = features["input_mask"]
#             input_type_ids = features["input_type_ids"]
#
#             model = modeling.BertModel(
#                 config=bert_config,
#                 is_training=False,
#                 input_ids=input_ids,
#                 input_mask=input_mask,
#                 token_type_ids=input_type_ids,
#                 use_one_hot_embeddings=use_one_hot_embeddings)
#
#             if mode != tf.estimator.ModeKeys.PREDICT:
#                 raise ValueError("Only PREDICT modes are supported: %s" % (mode))
#
#             tvars = tf.trainable_variables()
#             scaffold_fn = None
#             (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(
#                 tvars, init_checkpoint)
#             tf.train.init_from_checkpoint(init_checkpoint, assignment_map)
#
#             tf.logging.info("**** Trainable Variables ****")
#             for var in tvars:
#                 init_string = ""
#                 if var.name in initialized_variable_names:
#                     init_string = ", *INIT_FROM_CKPT*"
#                 tf.logging.info("  name = %s, shape = %s%s", var.name, var.shape, init_string)
#
#             all_layers = model.get_all_encoder_layers()
#
#             predictions = {
#                 "unique_id": unique_ids,
#             }
#
#             for (i, layer_index) in enumerate(layer_indexes):
#                 predictions["layer_output_%d" % i] = all_layers[layer_index]
#
#             output_spec = tf.contrib.tpu.TPUEstimatorSpec(
#                 mode=mode, predictions=predictions, scaffold_fn=scaffold_fn)
#             return output_spec
#
#     return model_fn


def convert_lst_to_features(lst_str: Union[List[List[str]], List[str]], max_seq_length: int, tokenizer: tokenization,
                            mask_cls_sep: bool = False):
    """Loads a data file into a list of `InputBatch`s."""
    examples = _read_tokenized_examples(lst_str)

    _tokenize = lambda x: tokenizer.mark_unk_tokens(x)
    all_tokens = [(ex.unique_id, _tokenize(ex.text_a), _tokenize(ex.text_b) if ex.text_b else []) for ex in examples]

    assert max_seq_length > 0

    for (unique_id, tokens_a, tokens_b) in all_tokens:
        if tokens_b:
            # Modifies `tokens_a` and `tokens_b` in place so that the total
            # length is less than the specified length.
            # Account for [CLS], [SEP], [SEP] with "- 3"
            _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        else:
            # Account for [CLS] and [SEP] with "- 2"
            if len(tokens_a) > max_seq_length - 2:
                tokens_a = tokens_a[0:(max_seq_length - 2)]

        # The convention in BERT is:
        # (a) For sequence pairs:
        #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
        #  type_ids: 0     0  0    0    0     0       0 0     1  1  1  1   1 1
        # (b) For single sequences:
        #  tokens:   [CLS] the dog is hairy . [SEP]
        #  type_ids: 0     0   0   0  0     0 0
        #
        # Where "type_ids" are used to indicate whether this is the first
        # sequence or the second sequence. The embedding vectors for `type=0` and
        # `type=1` were learned during pre-training and are added to the wordpiece
        # embedding vector (and position vector). This is not *strictly* necessary
        # since the [SEP] token unambiguously separates the sequences, but it makes
        # it easier for the model to learn the concept of sequences.
        #
        # For classification tasks, the first vector (corresponding to [CLS]) is
        # used as as the "sentence vector". Note that this only makes sense because
        # the entire model is fine-tuned.
        tokens = ['[CLS]'] + tokens_a + ['[SEP]']
        input_type_ids = [0] * len(tokens)
        input_mask = [int(not mask_cls_sep)] + [1] * len(tokens_a) + [int(not mask_cls_sep)]

        if tokens_b:
            tokens += tokens_b + ['[SEP]']
            input_type_ids += [1] * (len(tokens_b) + 1)
            input_mask += [1] * len(tokens_b) + [int(not mask_cls_sep)]

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # Zero-pad up to the sequence length. more pythonic
        pad_len = max_seq_length - len(input_ids)
        input_ids += [0] * pad_len
        input_mask += [0] * pad_len
        input_type_ids += [0] * pad_len

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(input_type_ids) == max_seq_length

        tf.logging.info("unique_id: %s" % unique_id)
        tf.logging.info("tokens: %s" % " ".join([tokenization.printable_text(x) for x in tokens]))
        tf.logging.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
        tf.logging.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
        tf.logging.info("input_type_ids: %s" % " ".join([str(x) for x in input_type_ids]))

        yield InputFeatures(
            unique_id=unique_id,
            tokens=tokens,
            input_ids=input_ids,
            input_mask=input_mask,
            input_type_ids=input_type_ids
        )


def _truncate_seq_pair(tokens_a: List[str], tokens_b: List[str], max_length: int):
    """Truncates a sequence pair in place to the maximum length."""

    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


def _read_examples(lst_strs: List[str]):
    """Read a list of `InputExample`s from a list of strings."""
    unique_id = 0
    for ss in lst_strs:
        line = tokenization.convert_to_unicode(ss)
        if not line:
            continue
        line = line.strip()
        text_a = None
        text_b = None
        m = re.match(r"^(.*) \|\|\| (.*)$", line)
        if m is None:
            text_a = line
        else:
            text_a = m.group(1)
            text_b = m.group(2)

        yield InputExample(unique_id=unique_id, text_a=text_a, text_b=text_b)
        unique_id += 1


def _read_tokenized_examples(lst_strs: List[List[str]]):
    unique_id = 0
    lst_strs = [[tokenization.convert_to_unicode(w) for w in s] for s in lst_strs]
    for ss in lst_strs:
        text_a = ss
        text_b = None
        try:
            j = ss.index('|||')
            text_a = ss[:j]
            text_b = ss[(j + 1):]
        except ValueError:
            pass
        yield InputExample(unique_id=unique_id, text_a=text_a, text_b=text_b)
        unique_id += 1


# def main(_):
#     vocab_file = '../../bert/models/vocab.txt'
#     do_lower_case = True
#     init_checkpoint = '../../bert/models/bert_model.ckpt'
#     layer_indexes = [-1, -2, -3, -4]
#     batch_size = 32
#     bert_config_file = '../../bert/models/bert_config.json'
#     max_seq_length = 256
#
#     # import os
#     # os.environ['CUDA_VISIBLE_DEVICES'] = "2"
#     tf.logging.set_verbosity(tf.logging.INFO)
#     tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)
#
#     bert_config = modeling.BertConfig.from_json_file(bert_config_file)
#     run_config = tf.contrib.tpu.RunConfig(
#         session_config=tf.ConfigProto(
#             allow_soft_placement=False,
#             # log_device_placement=True
#         )
#     )
#
#     model_fn = model_fn_builder(
#         bert_config=bert_config,
#         init_checkpoint=init_checkpoint,
#         layer_indexes=layer_indexes,
#         use_one_hot_embeddings=False
#     )
#
#     estimator = tf.estimator.Estimator(
#         model_fn=model_fn,
#         config=run_config
#     )
#     estimator = tf.contrib.tpu.TPUEstimator(
#         use_tpu=False,
#         model_fn=model_fn,
#         config=run_config,
#         predict_batch_size=batch_size
#     )
#
#     sentences = ['test', 'test2', 'test3', 'test4']
#     input_fn, tmp = input_fn_builder(sentences, tokenizer, max_seq_length=max_seq_length)
#     for result in estimator.predict(input_fn, yield_single_examples=True):
#         print(result.keys())
#         unique_id = result['unique_id']
#         feature = tmp[unique_id]
#         all_features = []
#         for (i, token) in enumerate(feature.tokens):
#             print(token)
#             all_layers = []
#             for (j, layer_index) in enumerate(layer_indexes):
#                 layer_output = result["layer_output_%d" % j]
#                 layers = collections.OrderedDict()
#                 layers["index"] = layer_index
#                 layers["values"] = layer_output[i:(i+1)]
#                 all_layers.append(layers)
#             tmp_features = collections.OrderedDict()
#             tmp_features["token"] = token
#             tmp_features["layers"] = all_layers
#             all_features.append(tmp_features)
#
#
# if __name__ == "__main__":
#     tf.app.run()
