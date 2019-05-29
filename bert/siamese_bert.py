from bert.bert import BertEncoder
from bert import tokenization
from bert import modeling
from bert import optimization

from typing import List
import tensorflow as tf


def _create_model(bert_config, init_checkpoint, layer_indexes, _input_ids, _input_mask, _input_type_ids,
                  _mention_mask, use_one_hot_embeddings: bool = False, scope: str = None):
    # Load the Bert Model
    model = modeling.BertModel(
        config=bert_config,
        is_training=False,
        input_ids=_input_ids,
        input_mask=_input_mask,
        token_type_ids=_input_type_ids,
        use_one_hot_embeddings=use_one_hot_embeddings,
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

    mention_embedding_layer = tf.div(tf.reduce_sum(output_layer * tf.expand_dims(_mention_mask, -1), axis=1),
                                     tf.expand_dims(tf.reduce_sum(_mention_mask, axis=1), axis=-1))

    return mention_embedding_layer


def model_fn_builder(bert_config, init_checkpoint, layer_indexes, learning_rate, num_train_steps,
                     num_warmup_steps, use_one_hot_embeddings):
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

        # Create siamese Bert Model
        with tf.variable_scope("siamese") as scope:
            output_layer_left = _create_model(bert_config, init_checkpoint, layer_indexes, input_ids_left,
                                              input_mask_left, input_type_ids_left, mention_mask_left,
                                              use_one_hot_embeddings, scope="bert")
            scope.reuse_variables()
            output_layer_right = _create_model(bert_config, init_checkpoint, layer_indexes, input_ids_right,
                                               input_mask_right, input_type_ids_right, mention_mask_right,
                                               use_one_hot_embeddings, scope="bert")

        # Create loss
        # FIXME: set margin in the config file
        loss = tf.contrib.losses.metric_learning.contrastive_loss(labels=labels,
                                                                  embeddings_anchor=output_layer_left,
                                                                  embeddings_positive=output_layer_right,
                                                                  margin=0.2)

        tvars = tf.trainable_variables()
        initialized_variable_names = {}
        scaffold_fn = None
        if init_checkpoint:
            (assignment_map, initialized_variable_names
             ) = modeling.get_assignment_map_from_checkpoint(tvars, init_checkpoint)
            tf.train.init_from_checkpoint(init_checkpoint, assignment_map)

        tf.logging.info("*** Trainable Variables ***")
        for var in tvars:
            init_string = ""
            if var.name in initialized_variable_names:
                init_string = ", *INIT_FROM_CKPT*"
            tf.logging.info("   name = %s, shape = %s%s", var.name, var.shape, init_string)

        train_op = optimization.create_optimizer(
            loss, learning_rate, num_train_steps, num_warmup_steps, False
        )

        output_spec = tf.contrib.tpu.TPUEstimatorSpec(
            mode=mode,
            loss=loss,
            train_op=train_op,
            scaffold_fn=scaffold_fn
        )
        return output_spec

    return model_fn


class SiameseBert(BertEncoder):
    def __init__(self, bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int=32,
                 layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        # Define siamese model with shared weights
        with tf.variable_scope("siamese") as scope:
            self._output_layer_left, self._input_ids_left, self._input_mask_left, self._input_type_ids_left, \
                self._mention_mask_left = self._load_model(bert_config_file, init_checkpoint, scope='bert',
                                                           placeholder_name_add='_left',
                                                           use_one_hot_embeddings=use_one_hot_embeddings)
            print("First model loaded")
            scope.reuse_variables()
            self._output_layer_right, self._input_ids_right, self._input_mask_right, self._input_type_ids_right, \
                self._mention_mask_right = self._load_model(bert_config_file, init_checkpoint, scope='bert',
                                                            placeholder_name_add='_right',
                                                            use_one_hot_embeddings=use_one_hot_embeddings)
            print("Second model loaded with shared weights")

        # Create loss
        self._label = tf.placeholder(tf.float32, [None])
        # FIXME: set margin in the config file
        self._loss = tf.contrib.losses.metric_learning.contrastive_loss(labels=self._label,
                                                                        embeddings_anchor=self._output_layer_left,
                                                                        embeddings_positive=self._output_layer_right,
                                                                        margin=0.2)

        super(SiameseBert, self).__init__(bert_config_file, init_checkpoint, vocab_file, seq_len, batch_size,
                                          layer_indexes, use_one_hot_embeddings, do_lower_case, load_model=False)

    def train(self):
        # FIXME: params
        do_lower_case = True
        init_checkpoint = "../bert/models/bert_model.ckpt"
        max_seq_len = 256
        bert_config_file = "../bert/models/bert_config.json"
        output_dir = "../bert/models/finetuned"
        save_checkpoints_steps = 1000
        iterations_per_loop = 1000
        num_tpu_cores = 8
        train_batch_size = 32
        num_train_epochs = 3.0
        warmup_proportion = 0.1

        tf.logging.set_verbosity(tf.logging.INFO)
        tokenization.validate_case_matches_checkpoint(do_lower_case, init_checkpoint)

        # FIXME: bert_config is loaded in load_model
        bert_config = modeling.BertConfig.from_json_file(bert_config_file)
        if max_seq_len > bert_config.max_position_embeddings:
            raise ValueError(
                "Cannot use sequence length %d because the BERT model "
                "was only trained up to sequence length %d" %
                (max_seq_len, bert_config.max_position_embeddings))

        tf.gfile.MakeDirs(output_dir)
        # FIXME
        label_list = None

        tpu_cluster_resolver = None
        is_per_host = tf.contrib.tpu.InputPipelineConfig.PER_HOST_V2
        run_config = tf.contrib.tpu.RunConfig(
            cluster=None,
            master=None,
            model_dir=output_dir,
            save_checkpoints_steps=save_checkpoints_steps,
            tpu_config=tf.contrib.tpu.TPUConfig(
                iterations_per_loop=iterations_per_loop,
                num_shards=num_tpu_cores,
                per_host_input_for_training=is_per_host
            )
        )

        # FIXME
        train_examples = None
        num_train_steps = int(len(train_examples) / train_batch_size * num_train_epochs)
        num_warmup_steps = int(num_train_steps * warmup_proportion)

        # model_fn = model_fn_builder(
        #
        # )


    # def train(self):
    #     # FIXME: config params
    #     train_iter = 10
    #     batch_size = 1
    #     step = 10
    #
    #     # Setup Optimizer
    #     global_step = tf.Variable(0, trainable=False)
    #
    #     train_step = tf.train.MomentumOptimizer(0.01, 0.99, use_nesterov=True).minimize(self._loss,
    #                                                                                     global_step=global_step)
    #
    #     # Start Training
    #     saver = tf.train.Saver()
    #
    #     # Setup tensorboard
    #     tf.summary.scaler('step', global_step)
    #     tf.summary.scalar('loss', self._loss)
    #     for var in tf.trainable_variables():
    #         tf.summary.hisogram(var.op.name, var)
    #     merged = tf.summary.merge_all()
    #     writer = tf.summary.FileWriter('train.log', self._sess.graph)
    #
    #     # train iter
    #     for i in range(train_iter):
    #         # FIXME: next_batch
    #         batch_ids_left, batch_mask_left, batch_type_ids_left, batch_ids_right, batch_mask_right, \
    #         batch_type_ids_right, batch_similarity = self.next_batch(batch_size)
    #         _, l, summary_str = self._sess.run([train_step, self._loss, merged], feed_dict={
    #             self._input_ids_left:batch_ids_left,
    #             self._input_mask_left:batch_mask_left,
    #             self._input_type_ids_left:batch_type_ids_left,
    #             self._input_ids_right:batch_ids_right,
    #             self._input_mask_right:batch_mask_right,
    #             self._input_type_ids_right:batch_type_ids_right,
    #             self._label:batch_similarity
    #         })
    #         writer.add_summary(summary_str, i)
    #         print("\r#%d - Loss" % i, l)
    #
    #         if (i+1) % step == 0:
    #             # FIXME: validation
    #             print("TODO validation")
    #
    #         saver.save(self._sess, "siamese_model.ckpt")

    def next_batch(self, batch_size):
        # FIXME: right now just dummy
        sentences = [['Das', 'ist', 'ein', 'Test.'], ['Das', 'ist', 'ein', 'zweiter', 'Test.']]
        is_tokenized = True

        features = self.convert_lst_to_features(sentences, max_seq_length=self._seq_len, tokenizer=self._tokenizer,
                                                is_tokenized=is_tokenized)
        pass
