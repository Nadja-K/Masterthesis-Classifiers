import configparser
import time
import json
import logging
import tensorflow as tf
import argparse
from configs.logging_config import logging_config
from logging.config import dictConfig
import ast

from classifiers.hybrid_classifier import HybridClassifier
from classifiers.bert_classifier import BertEmbeddingClassifier
from classifiers.token_classifier import TokenLevelEmbeddingClassifier
from classifiers.rule_classifier import RuleClassifier
from classifiers.rule_classifier import HeuristicPunctuation, HeuristicStemming, HeuristicSort, HeuristicStopwords, \
    HeuristicAbbreviationsCompounds, HeuristicAbbreviationsSpaces, HeuristicOriginal, HeuristicBrackets, \
    HeuristicLowercasing, HeuristicCorporateForms

# Logging
# logging.disable(logging.WARNING)

# Disable (most) Tensorflow Log messages
tf.logging.set_verbosity(tf.logging.ERROR)

# Config
config = configparser.ConfigParser()
# config.read("configs/config.ini")
config.read("configs/remote_config.ini")

# Global config settings that are used for all classifiers
dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')
skip_trivial_samples = config['DATASET'].getboolean('SKIP_TRIVIAL_SAMPLES', False)
dataset_split = config['DATASET'].get('SPLIT', 'val')
split_table_name = config['DATASET'].get('SPLIT_TABLE_NAME', 'splits')

eval_mode = config['EVALUATION'].get('MODE', 'mentions')
assert eval_mode in ['mentions', 'samples']
print(dataset_db_name)


def bert_embedding_classifier_main():
    # Settings
    annoy_metric = config['ANNOY'].get('ANNOY_METRIC', 'euclidean')
    num_trees = config['ANNOY'].getint('NUM_TREES', 30)
    annoy_index_path = config['ANNOY'].get('ANNOY_INDEX_PATH', None)
    annoy_output_dir = config['ANNOY'].get('ANNOY_OUTPUT_DIR', '')

    vocab_file = config['EMBEDDINGCLASSIFIER_BERT'].get('VOCAB_FILE', '')
    do_lower_case = config['EMBEDDINGCLASSIFIER_BERT'].getboolean('DO_LOWER_CASE', True)
    init_checkpoint = config['EMBEDDINGCLASSIFIER_BERT'].get('INIT_CHECKPOINT', '')
    layer_indexes = json.loads(config['EMBEDDINGCLASSIFIER_BERT'].get('LAYER_INDEXES', '[-1]'))
    batch_size = config['EMBEDDINGCLASSIFIER_BERT'].getint('BATCH_SIZE', 32)
    bert_config_file = config['EMBEDDINGCLASSIFIER_BERT'].get('BERT_CONFIG_FILE', '')
    seq_len = config['EMBEDDINGCLASSIFIER_BERT'].getint('SEQ_LEN', 256)
    use_one_hot_embeddings = config['EMBEDDINGCLASSIFIER_BERT'].get('USE_ONE_HOT_EMBEDDINGS', False)

    bert_distance_allowance = config['EMBEDDINGCLASSIFIER_BERT'].getfloat('DISTANCE_ALLOWANCE', None)
    num_results = config['EMBEDDINGCLASSIFIER_BERT'].getint('NUM_RESULTS', 1)

    # Argparse (this is optional and usually the config file is used - only use for experiments)
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_db_name', nargs='?', type=str, default=dataset_db_name)
    parser.add_argument('--dataset_split', nargs='?', type=str, default=dataset_split)
    parser.add_argument('--skip_trivial_samples', nargs='?', type=lambda x:ast.literal_eval(x), default=skip_trivial_samples)
    parser.add_argument('--vocab_file', nargs='?', type=str, default=vocab_file)
    parser.add_argument('--bert_config_file', nargs='?', type=str, default=bert_config_file)
    parser.add_argument('--init_checkpoint', nargs='?', type=str, default=init_checkpoint)
    parser.add_argument('--eval_mode', nargs='?', type=str, default=eval_mode)
    parser.add_argument('--layer_indexes', nargs='*', type=int, default=layer_indexes)
    args = parser.parse_args()
    print(args)

    # Logging
    dataset = args.dataset_db_name.split("/")[-1].split(".")[0]
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[0] + "_bert_embedding_" + dataset + ".log"
    dictConfig(logging_config)

    # Classifier
    classifier = BertEmbeddingClassifier(dataset_db_name=args.dataset_db_name, dataset_split=args.dataset_split,
                                         split_table_name=split_table_name,
                                         annoy_metric=annoy_metric, num_trees=num_trees,
                                         annoy_index_path=annoy_index_path, annoy_output_dir=annoy_output_dir,
                                         skip_trivial_samples=args.skip_trivial_samples,
                                         bert_config_file=args.bert_config_file, init_checkpoint=args.init_checkpoint,
                                         vocab_file=args.vocab_file, seq_len=seq_len, batch_size=batch_size,
                                         layer_indexes=args.layer_indexes, use_one_hot_embeddings=use_one_hot_embeddings,
                                         do_lower_case=do_lower_case,
                                         distance_allowance=bert_distance_allowance)
    start = time.time()
    classifier.evaluate_datasplit(args.dataset_split, num_results=num_results, eval_mode=args.eval_mode)
    print("Evaluation took %s" % (time.time() - start))
    # print(classifier.classify("test", "das ist ein test."))
    # print(classifier.multi_classify(['test'], 'das ist ein test.'))

    # Necessary to close the tensorflow session
    classifier.close_session()


def token_level_embedding_classifier_main():
    # Logging
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[0] + "_token_level_embedding.log"
    dictConfig(logging_config)

    # Settings
    embedding_model_path = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('EMBEDDING_MODEL_PATH', None)
    annoy_metric = config['ANNOY'].get('ANNOY_METRIC', 'euclidean')
    num_trees = config['ANNOY'].getint('NUM_TREES', 30)
    annoy_index_path = config['ANNOY'].get('ANNOY_INDEX_PATH', None)
    annoy_output_dir = config['ANNOY'].get('ANNOY_OUTPUT_DIR', '')
    use_compound_splitting = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getboolean('USE_COMPOUND_SPLITTING', False)
    compound_splitting_threshold = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getfloat('COMPOUND_SPLITTING_THRESHOLD', 0.5)
    distance_allowance = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getfloat('DISTANCE_ALLOWANCE', None)
    num_results = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getint('NUM_RESULTS', 1)

    # Argparse (this is optional and usually the config file is used - only use for experiments)
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_db_name', nargs='?', type=str, default=dataset_db_name)
    parser.add_argument('--dataset_split', nargs='?', type=str, default=dataset_split)
    parser.add_argument('--skip_trivial_samples', nargs='?', type=lambda x:ast.literal_eval(x), default=skip_trivial_samples)
    parser.add_argument('--eval_mode', nargs='?', type=str, default=eval_mode)
    args = parser.parse_args()
    print(args)

    # Classifier
    classifier = TokenLevelEmbeddingClassifier(dataset_db_name=args.dataset_db_name, dataset_split=args.dataset_split,
                                               split_table_name=split_table_name,
                                               embedding_model_path=embedding_model_path, annoy_metric=annoy_metric,
                                               num_trees=num_trees, annoy_index_path=annoy_index_path,
                                               annoy_output_dir=annoy_output_dir,
                                               skip_trivial_samples=args.skip_trivial_samples,
                                               use_compound_splitting=use_compound_splitting,
                                               compound_splitting_threshold=compound_splitting_threshold,
                                               distance_allowance=distance_allowance)
    start = time.time()
    classifier.evaluate_datasplit(args.dataset_split, num_results=num_results, eval_mode=args.eval_mode)
    print("Evaluation took %s" % (time.time() - start))


def rule_classifier_main():
    # Logging
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[0] + "_rule.log"
    dictConfig(logging_config)

    # Settings
    max_edit_distance_dictionary = config['RULECLASSIFIER'].getint('MAX_EDIT_DISTANCE_DICTIONARY', 5)
    abbreviations_max_edit_distance_dictionary = config['RULECLASSIFIER'].getint('ABBREVIATIONS_MAX_EDIT_'
                                                                                 'DISTANCE_DICTIONARY', 5)
    corporate_forms_list = json.loads(config['RULECLASSIFIER'].get('CORPORATE_FORMS_LIST', '[]'))
    prefix_length = config['RULECLASSIFIER'].getint('PREFIX_LENGTH', 5)
    count_threshold = config['RULECLASSIFIER'].getint('COUNT_THRESHOLD', 5)
    compact_level = config['RULECLASSIFIER'].getint('COMPACT_LEVEL', 5)
    compound_splitter_sensitivity = config['RULECLASSIFIER'].getfloat('COMPOUND_SPLITTING_THRESHOLD', 0.1)

    # Argparse (this is optional and usually the config file is used - only use for experiments)
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_db_name', nargs='?', type=str, default=dataset_db_name)
    parser.add_argument('--dataset_split', nargs='?', type=str, default=dataset_split)
    parser.add_argument('--skip_trivial_samples', nargs='?', type=lambda x:ast.literal_eval(x), default=skip_trivial_samples)
    parser.add_argument('--eval_mode', nargs='?', type=str, default=eval_mode)
    args = parser.parse_args()
    print(args)

    # Create heuristic objects
    original_heuristic = HeuristicOriginal(max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    corporate_forms_heuristic = HeuristicCorporateForms(max_edit_distance_dictionary, prefix_length, count_threshold,
                                                        compact_level, corporate_forms_list)
    brackets_heuristic = HeuristicBrackets(max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    punctuation_heuristic = HeuristicPunctuation(max_edit_distance_dictionary, prefix_length, count_threshold,
                                                 compact_level)
    lowercasing_heuristic = HeuristicLowercasing(max_edit_distance_dictionary, prefix_length, count_threshold,
                                                 compact_level)
    stemming_heuristic = HeuristicStemming(max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    stopword_heuristic = HeuristicStopwords(max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    sort_heuristic = HeuristicSort(max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    abbreviation_compounds_heuristic = HeuristicAbbreviationsCompounds(abbreviations_max_edit_distance_dictionary,
                                                                       prefix_length, count_threshold, compact_level,
                                                                       compound_splitter_sensitivity)
    abbreviation_spaces_heuristic = HeuristicAbbreviationsSpaces(abbreviations_max_edit_distance_dictionary,
                                                                 prefix_length, count_threshold, compact_level)

    # The order of the heuristics in this list matters because each heuristic will use the previous refactored string
    heuristic_list = [brackets_heuristic, punctuation_heuristic, corporate_forms_heuristic, lowercasing_heuristic,
                      stemming_heuristic, stopword_heuristic, sort_heuristic, abbreviation_compounds_heuristic,
                      abbreviation_spaces_heuristic]
    # heuristic_list = [original_heuristic]

    # Classifier
    classifier = RuleClassifier(heuristic_list, args.dataset_db_name, args.dataset_split, split_table_name,
                                args.skip_trivial_samples, False)
    start = time.time()
    classifier.evaluate_datasplit(args.dataset_split, eval_mode=args.eval_mode)
    print("Evaluation took %s" % (time.time() - start))


def hybrid_classifier():
    # Settings
    max_edit_distance_dictionary = config['RULECLASSIFIER'].getint('MAX_EDIT_DISTANCE_DICTIONARY', 5)
    abbreviations_max_edit_distance_dictionary = config['RULECLASSIFIER'].getint('ABBREVIATIONS_MAX_EDIT_'
                                                                                 'DISTANCE_DICTIONARY', 5)
    corporate_forms_list = json.loads(config['RULECLASSIFIER'].get('CORPORATE_FORMS_LIST', '[]'))
    prefix_length = config['RULECLASSIFIER'].getint('PREFIX_LENGTH', 5)
    count_threshold = config['RULECLASSIFIER'].getint('COUNT_THRESHOLD', 5)
    compact_level = config['RULECLASSIFIER'].getint('COMPACT_LEVEL', 5)
    compound_splitter_sensitivity = config['RULECLASSIFIER'].getfloat('COMPOUND_SPLITTING_THRESHOLD', 0.1)

    annoy_metric = config['ANNOY'].get('ANNOY_METRIC', 'euclidean')
    num_trees = config['ANNOY'].getint('NUM_TREES', 30)
    annoy_index_path = config['ANNOY'].get('ANNOY_INDEX_PATH', None)
    annoy_output_dir = config['ANNOY'].get('ANNOY_OUTPUT_DIR', '')

    vocab_file = config['EMBEDDINGCLASSIFIER_BERT'].get('VOCAB_FILE', '')
    do_lower_case = config['EMBEDDINGCLASSIFIER_BERT'].getboolean('DO_LOWER_CASE', True)
    init_checkpoint = config['EMBEDDINGCLASSIFIER_BERT'].get('INIT_CHECKPOINT', '')
    layer_indexes = json.loads(config['EMBEDDINGCLASSIFIER_BERT'].get('LAYER_INDEXES', '[-1]'))
    batch_size = config['EMBEDDINGCLASSIFIER_BERT'].getint('BATCH_SIZE', 32)
    bert_config_file = config['EMBEDDINGCLASSIFIER_BERT'].get('BERT_CONFIG_FILE', '')
    seq_len = config['EMBEDDINGCLASSIFIER_BERT'].getint('SEQ_LEN', 256)
    use_one_hot_embeddings = config['EMBEDDINGCLASSIFIER_BERT'].get('USE_ONE_HOT_EMBEDDINGS', False)

    bert_distance_allowance = config['EMBEDDINGCLASSIFIER_BERT'].getfloat('DISTANCE_ALLOWANCE', None)

    # Argparse (this is optional and usually the config file is used - only use for experiments)
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_db_name', nargs='?', type=str, default=dataset_db_name)
    parser.add_argument('--dataset_split', nargs='?', type=str, default=dataset_split)
    parser.add_argument('--skip_trivial_samples', nargs='?', type=lambda x:ast.literal_eval(x), default=skip_trivial_samples)
    parser.add_argument('--eval_mode', nargs='?', type=str, default=eval_mode)
    parser.add_argument('--vocab_file', nargs='?', type=str, default=vocab_file)
    parser.add_argument('--bert_config_file', nargs='?', type=str, default=bert_config_file)
    parser.add_argument('--init_checkpoint', nargs='?', type=str, default=init_checkpoint)
    parser.add_argument('--layer_indexes', nargs='*', type=int, default=layer_indexes)
    parser.add_argument('--max_edit_distance_dictionary', nargs='?', type=int, default=max_edit_distance_dictionary)
    args = parser.parse_args()
    print(args)

    # Logging
    dataset = args.dataset_db_name.split("/")[-1].split(".")[0]
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[
                                                                0] + "_hybrid_embedding_" + dataset + ".log"
    dictConfig(logging_config)
    print(logging_config['handlers']['fileHandler']['filename'])

    # Create heuristic objects
    original_heuristic = HeuristicOriginal(args.max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    corporate_forms_heuristic = HeuristicCorporateForms(args.max_edit_distance_dictionary, prefix_length, count_threshold,
                                                        compact_level, corporate_forms_list)
    brackets_heuristic = HeuristicBrackets(args.max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    punctuation_heuristic = HeuristicPunctuation(args.max_edit_distance_dictionary, prefix_length, count_threshold,
                                                 compact_level)
    lowercasing_heuristic = HeuristicLowercasing(args.max_edit_distance_dictionary, prefix_length, count_threshold,
                                                 compact_level)
    stemming_heuristic = HeuristicStemming(args.max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    stopword_heuristic = HeuristicStopwords(args.max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    sort_heuristic = HeuristicSort(args.max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
    abbreviation_compounds_heuristic = HeuristicAbbreviationsCompounds(abbreviations_max_edit_distance_dictionary,
                                                                       prefix_length, count_threshold, compact_level,
                                                                       compound_splitter_sensitivity)
    abbreviation_spaces_heuristic = HeuristicAbbreviationsSpaces(abbreviations_max_edit_distance_dictionary,
                                                                 prefix_length, count_threshold, compact_level)

    # The order of the heuristics in this list matters because each heuristic will use the previous refactored string
    heuristic_list = [brackets_heuristic, punctuation_heuristic, corporate_forms_heuristic, lowercasing_heuristic,
                      stemming_heuristic, stopword_heuristic, sort_heuristic, abbreviation_compounds_heuristic,
                      abbreviation_spaces_heuristic]
    # heuristic_list = [brackets_heuristic, punctuation_heuristic, corporate_forms_heuristic, lowercasing_heuristic,
    #                   stemming_heuristic, stopword_heuristic, sort_heuristic]
    # heuristic_list = [original_heuristic]

    # Classifier
    classifier = HybridClassifier(heuristics=heuristic_list, dataset_db_name=args.dataset_db_name,
                                  dataset_split=dargs.ataset_split, annoy_metric=annoy_metric,
                                  bert_config_file=args.bert_config_file, init_checkpoint=args.init_checkpoint,
                                  vocab_file=args.vocab_file, seq_len=seq_len, split_table_name=split_table_name,
                                  skip_trivial_samples=args.skip_trivial_samples, prefill_symspell=True,
                                  batch_size=batch_size, layer_indexes=args.layer_indexes,
                                  use_one_hot_embeddings=use_one_hot_embeddings, do_lower_case=do_lower_case,
                                  annoy_index_path=annoy_index_path, num_trees=num_trees,
                                  annoy_output_dir=annoy_output_dir, distance_allowance=bert_distance_allowance)

    start = time.time()
    print(classifier.classify("test", "das ist ein test"))
    classifier.evaluate_datasplit(args.dataset_split, eval_mode=args.eval_mode)
    print(classifier.classify("test", "das ist ein test"))
    print("Evaluation took %s" % (time.time() - start))


if __name__ == '__main__':
    # token_level_embedding_classifier_main()
    bert_embedding_classifier_main()
    # rule_classifier_main()
    # hybrid_classifier()
