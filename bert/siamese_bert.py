from bert.bert import BertEncoder
from bert import tokenization
from bert import modeling
from bert import optimization

from typing import List
import tensorflow as tf


class SiameseBert(BertEncoder):
    def __init__(self, bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int=32,
                 layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True):
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes

        # Define siamese model with shared weights
        with tf.variable_scope("") as scope:
            # FIXME
            self._output_layer_left, self._input_ids_left, self._input_mask_left, self._input_type_ids_left, \
                self._mention_mask_left = BertEncoder.load_model(bert_config_file, init_checkpoint, scope='bert',
                                                          placeholder_name_add='_left',
                                                          use_one_hot_embeddings=use_one_hot_embeddings)
            print("First model loaded")
            scope.reuse_variables()
            # FIXME
            self._output_layer_right, self._input_ids_right, self._input_mask_right, self._input_type_ids_right, \
                self._mention_mask_right = BertEncoder.load_model(bert_config_file, init_checkpoint, scope='bert',
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
