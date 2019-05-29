from bert.bert import BertEncoder
from bert import tokenization
from bert import modeling
from bert import optimization
from bert.extract_features import convert_lst_to_features

from typing import List, Tuple
import tensorflow as tf
import re
import logging
import numpy as np

log = logging.getLogger(__name__)


def _create_model(bert_config, init_checkpoint: str, layer_indexes, _input_ids, _input_mask, _input_type_ids,
                  _mention_mask, scope: str = None):
    # Load the Bert Model
    model = modeling.BertModel(
        config=bert_config,
        is_training=False,
        input_ids=_input_ids,
        input_mask=_input_mask,
        token_type_ids=_input_type_ids,
        use_one_hot_embeddings=False,
        scope=scope
    )
    tvars = tf.trainable_variables()

    # Load the checkpoint
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
    tvars = tf.trainable_variables()
    tf.logging.info(initialized_variable_names)
    tf.logging.info("*** Trainable Variables ***")
    for var in tvars:
        init_string = ""
        if var.name in initialized_variable_names:
            init_string = ", *INIT_FROM_CKPT*"
        tf.logging.info("   name = %s, shape = %s%s", var.name, var.shape, init_string)

    mention_embedding_layer = tf.div(tf.reduce_sum(output_layer * tf.expand_dims(_mention_mask, -1), axis=1),
                                     tf.expand_dims(tf.reduce_sum(_mention_mask, axis=1), axis=-1))

    return mention_embedding_layer


def model_fn_builder(bert_config, init_checkpoint, layer_indexes, learning_rate, num_train_steps,
                     num_warmup_steps):
    """Returns `model_fn` closure for TPUEstimator."""

    def model_fn(features, labels, mode, params):
        """The `model_fn` for TPUEstimator."""
        if mode != tf.estimator.ModeKeys.TRAIN:
            raise ValueError("Only TRAIN mode is supported: %s" % mode)

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
        with tf.variable_scope("siamese") as scope:
            output_layer_left = _create_model(bert_config, init_checkpoint, layer_indexes, input_ids_left,
                                              input_mask_left, input_type_ids_left, mention_mask_left,
                                              scope="bert")
            scope.reuse_variables()
            output_layer_right = _create_model(bert_config, init_checkpoint, layer_indexes, input_ids_right,
                                               input_mask_right, input_type_ids_right, mention_mask_right,
                                               scope="bert")

        # Create loss
        # FIXME: set margin in the config file
        loss = tf.contrib.losses.metric_learning.contrastive_loss(labels=label,
                                                                  embeddings_anchor=output_layer_left,
                                                                  embeddings_positive=output_layer_right,
                                                                  margin=2.0)

        loss = tf.Print(loss, [loss], message="loss values:")

        train_op = optimization.create_optimizer(
            loss, learning_rate, num_train_steps, num_warmup_steps, False
        )

        output_spec = tf.contrib.tpu.TPUEstimatorSpec(
            mode=mode,
            loss=loss,
            train_op=train_op,
            scaffold_fn=None
        )
        return output_spec

    return model_fn


def input_fn_builder(mentions: List[Tuple[str, str]], original_sentences: List[Tuple[str, str, int]], tokenizer: tokenization.FullTokenizer,
                     max_seq_length: int, drop_remainder: bool):

    def gen():
        for (m1, m2), (s1, s2, label) in zip(mentions, original_sentences):
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
            print(m1, s1)
            print(m2, s2)

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
        # d = d.batch(batch_size=batch_size, drop_remainder=drop_remainder)
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
    def __init__(self, bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int = 32,
                 layer_indexes: List[int] = [-1, -2, -3, -4], use_one_hot_embeddings: bool = False,
                 do_lower_case: bool = True):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        # FIXME: params
        self._do_lower_case = True
        self._init_checkpoint = "../bert/models/bert_model.ckpt"
        self._bert_config_file = "../bert/models/bert_config.json"
        self._output_dir = "../bert/models/finetuned"
        self._save_checkpoints_steps = 1000
        self._iterations_per_loop = 1
        self._num_tpu_cores = 8
        self._num_train_epochs = 1.0
        self._warmup_proportion = 0.1
        self._learning_rate = 2e-5

        self._tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)

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

        is_per_host = tf.contrib.tpu.InputPipelineConfig.PER_HOST_V2
        run_config = tf.contrib.tpu.RunConfig(
            cluster=None,
            master=None,
            model_dir=self._output_dir,
            save_checkpoints_steps=self._save_checkpoints_steps,
            tpu_config=tf.contrib.tpu.TPUConfig(
                iterations_per_loop=self._iterations_per_loop,
                num_shards=self._num_tpu_cores,
                per_host_input_for_training=is_per_host
            )
        )

        # FIXME: train_examples
        train_examples = None
        train_examples = [
                ('Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                 1),
                ('Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                 'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.',
                 0
                ),
                ('Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                 'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.',
                 0
                ),
                ('Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.',
                 'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.',
                 1
                )
            ]
        num_train_steps = int(len(train_examples) / self._batch_size * self._num_train_epochs)
        num_warmup_steps = int(num_train_steps * self._warmup_proportion)

        model_fn = model_fn_builder(
            bert_config=bert_config,
            init_checkpoint=self._init_checkpoint,
            layer_indexes=self._layer_indexes,
            learning_rate=self._learning_rate,
            num_train_steps=num_train_steps,
            num_warmup_steps=num_warmup_steps
        )

        estimator = tf.contrib.tpu.TPUEstimator(
            use_tpu=False,
            model_fn=model_fn,
            config=run_config,
            train_batch_size=self._batch_size,
            eval_batch_size=self._batch_size,
            predict_batch_size=self._batch_size
        )

        tf.logging.info("***** Running training *****")
        tf.logging.info("   Num examples = %d", len(train_examples))
        tf.logging.info("   Batch size = %d", self._batch_size)
        tf.logging.info("   Num steps = %d", num_train_steps)
        # FIXME
        train_input_fn = input_fn_builder(
            mentions=[('Binärbäume', 'Baum'), ('Binärbäume', 'Baum')],
            original_sentences=train_examples,
            tokenizer=self._tokenizer,
            max_seq_length=self._seq_len,
            drop_remainder=True
        )
        estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)
