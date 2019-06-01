from bert.train_siamese_bert import SiameseBert
import configparser
import json
import os

os.environ['CUDA_VISIBLE_DEVICES'] = "0"

# Config
config = configparser.ConfigParser()
config.read("configs/bert_train_config.ini")


def main():
    bert_config_file = config['TRAINING'].get('BERT_CONFIG_FILE', '')
    vocab_file = config['TRAINING'].get('VOCAB_FILE', '')
    init_checkpoint = config['TRAINING'].get('INIT_CHECKPOINT', '')
    output_dir = config['TRAINING'].get('OUTPUT_DIR', '')

    do_lower_case = config['TRAINING'].getboolean('DO_LOWER_CASE', True)

    layer_indexes = json.loads(config['TRAINING'].get('LAYER_INDEXES', '[-1]'))
    batch_size = config['TRAINING'].getint('BATCH_SIZE', 32)
    seq_len = config['TRAINING'].getint('SEQ_LEN', 256)

    save_checkpoints_steps = config['TRAINING'].getint('SAVE_CHECKPOINTS_STEPS', 1000)
    summary_steps = config['TRAINING'].getint('SUMMARY_STEPS', 1)

    num_train_epochs = config['TRAINING'].getfloat('NUM_TRAIN_EPOCHS', 1.0)
    warmup_proportion = config['TRAINING'].getfloat('WARMUP_PROPORTION', 0.1)
    learning_rate = config['TRAINING'].getfloat('LEARNING_RATE', 2e-6)
    margin = config['TRAINING'].getfloat('MARGIN', 2.0)

    be = SiameseBert(bert_config_file=bert_config_file, init_checkpoint=init_checkpoint, vocab_file=vocab_file,
                     output_dir=output_dir, seq_len=seq_len, batch_size=batch_size, layer_indexes=layer_indexes,
                     do_lower_case=do_lower_case, num_train_epochs=num_train_epochs, summary_steps=summary_steps,
                     warmup_proportion=warmup_proportion, save_checkpoints_steps=save_checkpoints_steps,
                     learning_rate=learning_rate, margin=margin)
    be.train()


if __name__ == "__main__":
    main()
