from bert.train_siamese_bert import SiameseBert
import configparser
import json
import os

# os.environ['CUDA_VISIBLE_DEVICES'] = "0"
os.environ['CUDA_VISIBLE_DEVICES'] = "1"
# os.environ['CUDA_VISIBLE_DEVICES'] = "7"

# Config
config = configparser.ConfigParser()
config.read("configs/bert_train_config.ini")


# FIXME: distributed multi-gpu training
# https://github.com/horovod/horovod
# https://github.com/horovod/horovod/blob/master/examples/tensorflow_mnist_estimator.py

def main():
    # Global config settings that are used for all classifiers
    dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')
    skip_trivial_samples = config['DATASET'].getboolean('SKIP_TRIVIAL_SAMPLES', False)
    dataset_split = config['DATASET'].get('SPLIT', 'val')
    split_table_name = config['DATASET'].get('SPLIT_TABLE_NAME', 'splits')
    num_query_sentences_per_entity = config['DATASET'].getint('NUM_QUERY_SENTENCES_PER_ENTITY', 2)
    print(dataset_db_name)

    bert_config_file = config['TRAINING'].get('BERT_CONFIG_FILE', '')
    vocab_file = config['TRAINING'].get('VOCAB_FILE', '')
    init_checkpoint = config['TRAINING'].get('INIT_CHECKPOINT', '')
    output_dir = config['TRAINING'].get('OUTPUT_DIR', '')

    do_lower_case = config['TRAINING'].getboolean('DO_LOWER_CASE', True)

    layer_indexes = json.loads(config['TRAINING'].get('LAYER_INDEXES', '[-1]'))
    batch_size = config['TRAINING'].getint('BATCH_SIZE', 30)
    seq_len = config['TRAINING'].getint('SEQ_LEN', 256)

    save_checkpoints_steps = config['TRAINING'].getint('SAVE_CHECKPOINTS_STEPS', 1000)
    summary_steps = config['TRAINING'].getint('SUMMARY_STEPS', 1)

    num_train_epochs = config['TRAINING'].getfloat('NUM_TRAIN_EPOCHS', 1.0)
    num_train_steps = config['TRAINING'].getfloat('NUM_TRAIN_STEPS', None)
    warmup_proportion = config['TRAINING'].getfloat('WARMUP_PROPORTION', 0.1)
    learning_rate = config['TRAINING'].getfloat('LEARNING_RATE', 2e-6)
    margin = config['TRAINING'].getfloat('MARGIN', 2.0)
    loss = config['TRAINING'].get('LOSS', 'cosine_contrastive')
    beta = config['TRAINING'].getfloat('BETA', 1.0)

    steps_per_eval_iter = config['EVALUATION'].getint('STEPS_PER_EVAL_ITER', 10)

    be = SiameseBert(bert_config_file=bert_config_file, init_checkpoint=init_checkpoint, vocab_file=vocab_file,
                     output_dir=output_dir, seq_len=seq_len, batch_size=batch_size, layer_indexes=layer_indexes,
                     do_lower_case=do_lower_case, num_train_epochs=num_train_epochs, summary_steps=summary_steps,
                     warmup_proportion=warmup_proportion, save_checkpoints_steps=save_checkpoints_steps,
                     learning_rate=learning_rate, margin=margin, dataset_db_name=dataset_db_name,
                     dataset_split=dataset_split, skip_trivial_samples=skip_trivial_samples,
                     split_table_name=split_table_name, steps_per_eval_iter=steps_per_eval_iter,
                     loss=loss, beta=beta, num_train_steps=num_train_steps,
                     num_query_sentences_per_entity=num_query_sentences_per_entity)
    be.train()


if __name__ == "__main__":
    main()
