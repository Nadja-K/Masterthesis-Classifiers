from bert import tokenization
from bert import modeling
from bert import optimization
from bert.extract_features import convert_lst_to_features
from bert.bert import BertEncoder
from classifiers.classifier import Classifier

from typing import List, Tuple, Dict, Union, Set
import tensorflow as tf
from tensorflow.python.ops import math_ops
import re
import logging
import numpy as np
import random

log = logging.getLogger(__name__)


def model_fn_builder(bert_config, init_checkpoint, layer_indexes, learning_rate, num_train_steps,
                     num_warmup_steps, summary_steps, margin):
    """Returns `model_fn` closure for Estimator."""
    def custom_contrastive_loss(labels, embeddings_anchor, embeddings_positive, margin=2.0):
        """
        Computes the angular contrastive loss as opposed to the standard implementation
        that uses the euclidean distance between two samples.

        Args:
            labels: 1-D tf.int32 `Tensor` with shape [batch_size] of
                binary labels indicating positive vs negative pair.
            embeddings_anchor: 2-D float `Tensor` of embedding vectors for the anchor
                images. Embeddings should be l2 normalized.
            embeddings_positive: 2-D float `Tensor` of embedding vectors for the
                positive images. Embeddings should be l2 normalized.
            margin: margin term in the loss definition.

        Returns:
            contrastive_loss: tf.float32 scalar.
        """
        # Get per pair distances
        # Note: the max margin for the cosine distance should be 2
        distances = tf.reshape(tf.losses.cosine_distance(tf.nn.l2_normalize(embeddings_anchor, dim=1),
                                                         tf.nn.l2_normalize(embeddings_positive, dim=1), axis=1,
                                                         reduction=tf.losses.Reduction.NONE), [-1])

        distances = tf.Print(distances, [distances], message="cosine distances:", summarize=10)
        # Add contrastive loss for the siamese network.
        #   label here is {0,1} for neg, pos.
        return math_ops.reduce_mean(
            math_ops.to_float(labels) * math_ops.square(distances) +
            (1. - math_ops.to_float(labels)) *
            math_ops.square(math_ops.maximum(margin - distances, 0.)),
            name='contrastive_loss')

    def model_fn(features, labels, mode, params):
        """The `model_fn` for Estimator."""
        tf.logging.info("*** Features ***")
        for name in sorted(features.keys()):
            tf.logging.info("  name = %s, shape = %s" % (name, features[name].shape))

        input_ids_left = features["input_ids_left"]
        input_mask_left = features["input_mask_left"]
        input_type_ids_left = features["input_type_ids_left"]
        mention_mask_left = features["mention_mask_left"]

        input_ids_right = features["input_ids_right"]
        input_mask_right = features["input_mask_right"]
        input_type_ids_right = features["input_type_ids_right"]
        mention_mask_right = features["mention_mask_right"]

        label = features["label"]

        # Create siamese Bert Model
        # Note: ONLY USE AN EMPTY SCOPE HERE! EVERYTHING ELSE WILL BREAK CHECKPOINT RELOADING!!!
        with tf.variable_scope("") as scope:
            output_layer_left = BertEncoder.load_model(bert_config=bert_config, init_checkpoint=init_checkpoint,
                                                       layer_indexes=layer_indexes, input_ids=input_ids_left,
                                                       input_mask=input_mask_left, input_type_ids=input_type_ids_left,
                                                       mention_mask=mention_mask_left, scope="bert", is_training=True)
            scope.reuse_variables()
            # FIXME: make sure that NOT loading the checkpoint for the 2nd network is 'fine'
            output_layer_right = BertEncoder.load_model(bert_config=bert_config, init_checkpoint=None,
                                                        layer_indexes=layer_indexes, input_ids=input_ids_right,
                                                        input_mask=input_mask_right, input_type_ids=input_type_ids_right,
                                                        mention_mask=mention_mask_right, scope="bert", is_training=True)

        # Create loss
        with tf.variable_scope("loss"):
            loss = custom_contrastive_loss(labels=label, embeddings_anchor=output_layer_left,
                                           embeddings_positive=output_layer_right, margin=margin)
            # loss = tf.contrib.losses.metric_learning.contrastive_loss(labels=label,
            #                                                           embeddings_anchor=output_layer_left,
            #                                                           embeddings_positive=output_layer_right,
            #                                                           margin=margin)

        if mode == tf.estimator.ModeKeys.TRAIN:
            loss = tf.Print(loss, [features["label"]], message="Label:", summarize=10)
            loss = tf.Print(loss, [loss], message="Loss value:")

            train_op = optimization.create_optimizer(
                loss, learning_rate, num_train_steps, num_warmup_steps, False
            )

            # Adds a logging hook for the loss during training
            logging_hook = tf.train.LoggingTensorHook({"train_loss": loss}, every_n_iter=summary_steps, at_end=True)
            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                loss=loss,
                train_op=train_op,
                training_hooks=[logging_hook]
            )
        elif mode == tf.estimator.ModeKeys.EVAL:
            mean_loss = tf.metrics.mean(loss)
            metrics = {'eval_loss': mean_loss}
            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                loss=loss,
                eval_metric_ops=metrics
            )
        else:
            raise ValueError("Only TRAIN and EVAL mode are supported: %s" % mode)

        return output_spec

    return model_fn


def input_fn_builder(samples: List[Union[Tuple[Set[str], int]]], tokenizer: tokenization.FullTokenizer,
                     max_seq_length: int, drop_remainder: bool):

    def gen():
        for sample in samples:
            l_r_sample = list(sample[0])
            m1, s1 = l_r_sample[0]
            m2, s2 = l_r_sample[1]
            m1 = str(m1)
            m2 = str(m2)
            s1 = str(s1)
            s2 = str(s2)
            label = sample[1]

            tokens1, mapping1 = tokenizer.tokenize(s1)
            tokens2, mapping2 = tokenizer.tokenize(s2)

            # Update the mapping with the CLS and SEP tag
            mapping1 = [('[CLS]', 0)] + [(token, token_index+1) for (token, token_index) in
                                         mapping1] + [('[SEP]', mapping1[-1][1]+2)]
            mapping2 = [('[CLS]', 0)] + [(token, token_index+1) for (token, token_index) in
                                         mapping2] + [('[SEP]', mapping2[-1][1]+2)]

            features = list(convert_lst_to_features([tokens1, tokens2], max_seq_length=max_seq_length, tokenizer=tokenizer))

            mention_mask1 = _get_mention_mask(max_seq_length, m1, s1, mapping1)
            mention_mask2 = _get_mention_mask(max_seq_length, m2, s2, mapping2)

            yield {
                'input_ids_left': [features[0].input_ids],
                'input_mask_left': [features[0].input_mask],
                'input_type_ids_left': [features[0].input_type_ids],
                'mention_mask_left': [mention_mask1],
                'input_ids_right': [features[1].input_ids],
                'input_mask_right': [features[1].input_mask],
                'input_type_ids_right': [features[1].input_type_ids],
                'mention_mask_right': [mention_mask2],
                'label': [label]
            }

    def input_fn(params):
        """The actual input function."""
        batch_size = params["batch_size"]

        d = (tf.data.Dataset.from_generator(
            gen,
            output_types={
                'input_ids_left': tf.int32,
                'input_mask_left': tf.int32,
                'input_type_ids_left': tf.int32,
                'mention_mask_left': tf.float32,
                'input_ids_right': tf.int32,
                'input_mask_right': tf.int32,
                'input_type_ids_right': tf.int32,
                'mention_mask_right': tf.float32,
                'label': tf.int32
            },
            output_shapes={
                'input_ids_left': (None, max_seq_length),
                'input_mask_left': (None, max_seq_length),
                'input_type_ids_left': (None, max_seq_length),
                'mention_mask_left': (None, max_seq_length),
                'input_ids_right': (None, max_seq_length),
                'input_mask_right': (None, max_seq_length),
                'input_type_ids_right': (None, max_seq_length),
                'mention_mask_right': (None, max_seq_length),
                'label': (None, )
            }
        ))

        d = d.repeat()
        d = d.shuffle(buffer_size=100)

        # Unbatch before batching is possible (bc of the (None, ...) definition above)
        d = d.apply(tf.data.experimental.unbatch())
        d = d.batch(batch_size=batch_size, drop_remainder=drop_remainder)
        return d

    return input_fn


def _get_mention_mask(seq_len: int, mention: str, sentence: str, token_mapping: List[Tuple[str, int]]) -> np.ndarray:
    mask = np.zeros(seq_len)

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

    if (phrase_start_token_index >= seq_len or phrase_end_token_index >= seq_len):
        log.warning("The current sample has more tokens than max_seq_len=%d allows and the mention seems "
                    "to be out of the boundaries in this case. Instead of an avg. phrase embedding, an avg. "
                    "sentence embedding will be returned.\n"
                    "Sentence: %s\n"
                    "Phrase: %s" % (seq_len, sentence, mention))
        mask = np.ones(seq_len)
    else:
        assert len(mask[phrase_start_token_index:phrase_end_token_index]) > 0, \
            "Something went wrong with the phrase embedding retrieval."

        mask[phrase_start_token_index:phrase_end_token_index] = 1

    return mask


class SiameseBert:
    def __init__(self, bert_config_file: str, init_checkpoint: str, dataset_db_name: str, dataset_split: str,
                 vocab_file: str, output_dir: str, split_table_name: str, skip_trivial_samples: bool = False,
                 seq_len: int = 256, batch_size: int = 32, layer_indexes: List[int] = [-1, -2, -3, -4],
                 learning_rate: float = 2e-6, num_train_epochs: float = 1.0, warmup_proportion: float = 0.1,
                 do_lower_case: bool = True, save_checkpoints_steps: int = 1000, summary_steps: int = 1,
                 margin: float = 2.0, steps_per_eval_iter: int = 10):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        self._do_lower_case = do_lower_case
        self._init_checkpoint = init_checkpoint
        self._bert_config_file = bert_config_file

        self._output_dir = output_dir
        self._save_checkpoints_steps = save_checkpoints_steps
        self._summary_steps = summary_steps

        self._num_train_epochs = num_train_epochs
        self._warmup_proportion = warmup_proportion
        self._learning_rate = learning_rate
        self._margin = margin

        self._steps_per_eval_iter = steps_per_eval_iter

        self._tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)

        assert dataset_split in ['train', 'test', 'val']
        train_query_data, train_context_data, train_entities, _ = Classifier.load_datasplit(
            dataset_db_name=dataset_db_name, dataset_split=dataset_split, split_table_name=split_table_name,
            skip_trivial_samples=skip_trivial_samples, load_context=False
        )
        self._training_data = self.generate_data_pairs(train_query_data, train_context_data, train_entities)

        # Only load the validation split if the training split has been specified
        self._validation_data = None
        if dataset_split == 'train':
            val_query_data, val_context_data, val_entities, _ = Classifier.load_datasplit(
                dataset_db_name=dataset_db_name, dataset_split='val', split_table_name=split_table_name,
                skip_trivial_samples=skip_trivial_samples, load_context=False
            )
            self._validation_data = self.generate_data_pairs(val_query_data, val_context_data, val_entities)

    def generate_data_pairs(self, query_data, context_data, entities):
        data_dict = {}

        def create_data_dict(data, data_dict):
            for sample in data:
                if sample['entity_title'] not in data_dict:
                    data_dict[sample['entity_title']] = set()
                data_dict[sample['entity_title']].add((sample['mention'], sample['sentence']))

        # Note: yes really on both because if a entity only has 2 samples in total and I would only use one of it I
        # would be unable to generate a positive pair sample
        create_data_dict(query_data, data_dict)
        create_data_dict(context_data, data_dict)

        data_pairs = []
        # FIXME: rework this .... ????
        for left_entity, entity_samples in data_dict.items():
            # FIXME: make the number a config parameter (to limit the number of pairwise samples per entity)
            num_query_sentences = min(2, int(len(entity_samples) / 2))
            num_pairs_per_query_sentence = 1
            positive_sample_pairs = []
            negative_sample_pairs = []

            # Pick a few query sentences, then pick a few positive and negative pair sentences for each query sentence
            while True:
                left_samples = random.sample(entity_samples, k=min(num_query_sentences, len(entity_samples)))
                for left_sample in left_samples:
                    # Positive samples
                    right_samples = list(entity_samples - set(left_samples))
                    right_samples = random.sample(right_samples, k=min(num_pairs_per_query_sentence, len(right_samples)))
                    for right_sample in right_samples:
                        positive_sample_pair = ({left_sample, right_sample}, 1)
                        # FIXME: make sure this is correct
                        # if positive_sample_pair not in positive_sample_pairs:
                        assert positive_sample_pair not in data_pairs
                        positive_sample_pairs.append(positive_sample_pair)

                # If at least one positive sample pair has been found for this entity, stop. Otherwise redo.
                if len(positive_sample_pairs) > 0:
                    break
                else:
                    # FIXME: check if this ever happens, otherwise just do an assert >= 1 positive sample pair
                    print("Redoing positive sampling for entity: %s" % left_entity)

            print("Found %s positive pairwise sample(s) for the entity '%s'." %
                  (len(positive_sample_pairs), left_entity))

            for left_sample in left_samples:
                # Negative samples
                seen_sentences = set()
                seen_entities = set()

                while True:
                    # pick a random negative sentence
                    while True:
                        # Get a random entity and a sample sentence for that random entity
                        right_entity = random.choices(list(entities - {left_entity}), k=1)[0]
                        possible_right_samples = data_dict[right_entity] - seen_sentences
                        seen_entities.add(right_entity)
                        if len(possible_right_samples) > 0 or ((len(seen_entities) - len(entities) + 1) == 0):
                            break
                    if len(possible_right_samples) == 0:
                        break
                    right_sample = random.choices(list(possible_right_samples), k=1)[0]

                    # If the sample is new, add it.
                    negative_sample_pair = ({left_sample, right_sample}, 0)
                    if negative_sample_pair not in data_pairs:
                        negative_sample_pairs.append(negative_sample_pair)
                    seen_sentences.add(right_sample)

                    # Stop if enough negative samples have been created or after 3 attempts of sampling a new sample
                    if len(seen_sentences) >= (len(positive_sample_pairs) / len(left_samples)):
                        break

            print("Found %s negative pairwise sample(s) for the entity '%s'." %
                  (len(negative_sample_pairs), left_entity))

            data_pairs.extend(positive_sample_pairs)
            data_pairs.extend(negative_sample_pairs)
            # FIXME: assert that at least 1 positive and 1 negative pairwise sample has been generated per entity

        # FIXME: remove this again later
        # for data_pair in data_pairs:
        #     print(list(data_pair[0])[0])
        #     print(list(data_pair[0])[1])
        #     print(data_pair[1])
        #     print("")

        print("Generated %s training pairs." % (len(data_pairs)))
        return data_pairs

    def train(self):
        tf.logging.set_verbosity(tf.logging.INFO)
        tokenization.validate_case_matches_checkpoint(self._do_lower_case, self._init_checkpoint)

        bert_config = modeling.BertConfig.from_json_file(self._bert_config_file)
        if self._seq_len > bert_config.max_position_embeddings:
            raise ValueError(
                "Cannot use sequence length %d because the BERT model "
                "was only trained up to sequence length %d" %
                (self._seq_len, bert_config.max_position_embeddings))

        tf.gfile.MakeDirs(self._output_dir)

        run_config = tf.estimator.RunConfig(
            model_dir=self._output_dir,
            save_checkpoints_steps=self._save_checkpoints_steps,
            save_summary_steps=self._summary_steps
        )

        num_train_steps = int(len(self._training_data) / self._batch_size * self._num_train_epochs)
        num_warmup_steps = int(num_train_steps * self._warmup_proportion)

        model_fn = model_fn_builder(
            bert_config=bert_config,
            init_checkpoint=self._init_checkpoint,
            layer_indexes=self._layer_indexes,
            learning_rate=self._learning_rate,
            num_train_steps=num_train_steps,
            num_warmup_steps=num_warmup_steps,
            summary_steps=self._summary_steps,
            margin=self._margin
        )

        estimator = tf.estimator.Estimator(
            model_fn=model_fn,
            model_dir=self._output_dir,
            config=run_config,
            params={'batch_size': self._batch_size}
        )

        tf.logging.info("***** Running training *****")
        tf.logging.info("   Num examples = %d", len(self._training_data))
        tf.logging.info("   Batch size = %d", self._batch_size)
        tf.logging.info("   Num steps = %d", num_train_steps)

        train_input_fn = input_fn_builder(
            samples=self._training_data,
            tokenizer=self._tokenizer,
            max_seq_length=self._seq_len,
            drop_remainder=True
        )
        if self._validation_data is None:
            estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)
        else:
            validation_input_fn = input_fn_builder(
                samples=self._validation_data,
                tokenizer=self._tokenizer,
                max_seq_length=self._seq_len,
                drop_remainder=True
            )
            train_spec = tf.estimator.TrainSpec(input_fn=train_input_fn, max_steps=num_train_steps)
            eval_spec = tf.estimator.EvalSpec(input_fn=validation_input_fn, steps=self._steps_per_eval_iter,
                                              start_delay_secs=0, throttle_secs=0)

            tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
