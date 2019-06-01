from bert import tokenization
from bert import modeling
from bert import optimization
from bert.extract_features import convert_lst_to_features
from classifiers.classifier import Classifier

from typing import List, Tuple, Dict, Union
import tensorflow as tf
from tensorflow.python.ops import math_ops
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
        with tf.variable_scope("loss"):
            loss = custom_contrastive_loss(labels=label, embeddings_anchor=output_layer_left,
                                           embeddings_positive=output_layer_right, margin=margin)
            # loss = tf.contrib.losses.metric_learning.contrastive_loss(labels=label,
            #                                                           embeddings_anchor=output_layer_left,
            #                                                           embeddings_positive=output_layer_right,
            #                                                           margin=margin)

        loss = tf.Print(loss, [features["label"]], message="Label:", summarize=10)
        loss = tf.Print(loss, [loss], message="Loss value:")

        train_op = optimization.create_optimizer(
            loss, learning_rate, num_train_steps, num_warmup_steps, False
        )

        # Adds a logging hook for the loss during training
        logging_hook = tf.train.LoggingTensorHook({"loss": loss}, every_n_iter=summary_steps, at_end=True)
        output_spec = tf.estimator.EstimatorSpec(
            mode=mode,
            loss=loss,
            train_op=train_op,
            training_hooks=[logging_hook]
        )
        return output_spec

    return model_fn


def input_fn_builder(samples: List[Dict[str, Union[str, int]]], tokenizer: tokenization.FullTokenizer,
                     max_seq_length: int, drop_remainder: bool):

    def gen():
        for sample in samples:
            s1 = sample['s1']
            s2 = sample['s2']
            m1 = sample['m1']
            m2 = sample['m2']
            label = sample['label']

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
                 margin: float = 2.0):
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

        self._tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)

        assert dataset_split in ['train', 'test', 'val']
        self._query_data, self._context_data, self._entities, self._loaded_datasplit = Classifier.load_datasplit(
            dataset_db_name=dataset_db_name, dataset_split=dataset_split, split_table_name=split_table_name,
            skip_trivial_samples=skip_trivial_samples, load_context=False
        )
        print(self._query_data)

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

        # FIXME: train_samples
        train_samples = [
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Die Darstellung des DNS-Namensraumes erfolgt als Wurzelbaum.',
                'm2': 'Wurzelbaum',
                'label': 1
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird.',
                'm2': 'Baumstruktur',
                'label': 1
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm1': 'Baum',
                's2': 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm1': 'Baum',
                's2': 'Die Darstellung des DNS-Namensraumes erfolgt als Wurzelbaum.',
                'm2': 'Wurzelbaum',
                'label': 1
            },
            {
                's1': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm1': 'Baum',
                's2': 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird.',
                'm2': 'Baumstruktur',
                'label': 1
            },
            {
                's1': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm1': 'Baum',
                's2': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Die Darstellung des DNS-Namensraumes erfolgt als Wurzelbaum.',
                'm2': 'Wurzelbaum',
                'label': 1
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird.',
                'm2': 'Baumstruktur',
                'label': 1
            },
            {
                's1': 'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.',
                'm1': 'Baum',
                's2': 'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.',
                'm1': 'Baum',
                's2': 'Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.',
                'm1': 'Baum',
                's2': 'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.',
                'm2': 'Baum',
                'label': 1
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.',
                'm2': 'Bäume',
                'label': 0
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird.',
                'm2': 'Bäume',
                'label': 0
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.',
                'm1': 'Bäume',
                's2': 'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird.',
                'm2': 'Bäume',
                'label': 0
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.',
                'm2': 'Bäume',
                'label': 0
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.',
                'm1': 'Baum',
                's2': 'Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm1': 'Baum',
                's2': 'Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm1': 'Baum',
                's2': 'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.',
                'm2': 'Baum',
                'label': 0
            },
            {
                's1': 'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.',
                'm1': 'Baum',
                's2': 'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.',
                'm2': 'Baum',
                'label': 0
            }
        ]
        num_train_steps = int(len(train_samples) / self._batch_size * self._num_train_epochs)
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
        tf.logging.info("   Num examples = %d", len(train_samples))
        tf.logging.info("   Batch size = %d", self._batch_size)
        tf.logging.info("   Num steps = %d", num_train_steps)
        train_input_fn = input_fn_builder(
            samples=train_samples,
            tokenizer=self._tokenizer,
            max_seq_length=self._seq_len,
            drop_remainder=True
        )
        estimator.train(input_fn=train_input_fn, max_steps=num_train_steps)
