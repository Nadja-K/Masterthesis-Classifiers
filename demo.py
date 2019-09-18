import configparser
import json
import tensorflow as tf
import argparse
import numpy as np
from configs.logging_config import logging_config
from logging.config import dictConfig

from classifiers.hybrid_classifier import HybridClassifier
from classifiers.bert_classifier import BertEmbeddingClassifier
from classifiers.rule_classifier import RuleClassifier
from classifiers.rule_classifier import HeuristicPunctuation, HeuristicStemming, HeuristicSort, HeuristicStopwords, \
    HeuristicAbbreviationsCompounds, HeuristicAbbreviationsSpaces, HeuristicBrackets, \
    HeuristicLowercasing, HeuristicCorporateForms

# Disable (most) Tensorflow Log messages
tf.logging.set_verbosity(tf.logging.ERROR)

# Config
config = configparser.ConfigParser()
config.read("configs/config.ini")

# Global config settings that are used for all classifiers
dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')
empolis_synonym_mapping_path = config['DATASET'].get('EMPOLIS_EVAL_MAPPING_FILE', None)
skip_trivial_samples = config['DATASET'].getboolean('SKIP_TRIVIAL_SAMPLES', False)
dataset_split = config['DATASET'].get('SPLIT', 'val')
split_table_name = config['DATASET'].get('SPLIT_TABLE_NAME', 'splits')

eval_mode = config['EVALUATION'].get('MODE', 'mentions')
assert eval_mode in ['mentions', 'samples']


def bert_embedding_classifier_main(mention, sentence, entity_synonyms, entity_synonyms_distance_threshold):
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

    # Logging
    dataset = dataset_db_name.split("/")[-1].split(".")[0]
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[0] + "_bert_embedding_" + dataset + ".log"
    dictConfig(logging_config)

    # Classifier
    classifier = BertEmbeddingClassifier(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                                         split_table_name=split_table_name,
                                         annoy_metric=annoy_metric, num_trees=num_trees,
                                         annoy_index_path=annoy_index_path, annoy_output_dir=annoy_output_dir,
                                         skip_trivial_samples=skip_trivial_samples,
                                         bert_config_file=bert_config_file, init_checkpoint=init_checkpoint,
                                         vocab_file=vocab_file, seq_len=seq_len, batch_size=batch_size,
                                         layer_indexes=layer_indexes, use_one_hot_embeddings=use_one_hot_embeddings,
                                         do_lower_case=do_lower_case,
                                         distance_allowance=bert_distance_allowance)

    if entity_synonyms is None:
        print(classifier.classify(mentions=mention, sentence=sentence))
    else:
        output = classifier.get_potential_synonyms(entity=entity_synonyms,
                                                   distance_threshold=entity_synonyms_distance_threshold)
        for mention, distances in output.items():
            print("Mention: %s | Avg. distance: %.2f" % (mention, np.average(distances['distances'])))

    # Necessary to close the tensorflow session
    classifier.close_session()


def rule_classifier_main(mention, sentence, entity_synonyms, entity_synonyms_distance_threshold):
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

    # Create heuristic objects
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

    # Classifier
    classifier = RuleClassifier(heuristic_list, dataset_db_name, dataset_split, split_table_name,
                                skip_trivial_samples, False)

    if entity_synonyms is None:
        print(classifier.classify(mentions=mention, sentence=sentence))
    else:
        output = classifier.get_potential_synonyms(entity=entity_synonyms,
                                                   distance_threshold=entity_synonyms_distance_threshold)
        for mention, distances in output.items():
            print("Mention: %s | Avg. distance: %.2f" % (mention, np.average(distances['distances'])))


def hybrid_classifier(mention, sentence, entity_synonyms, entity_synonyms_distance_threshold):
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


    # Logging
    dataset = dataset_db_name.split("/")[-1].split(".")[0]
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[
                                                                0] + "_hybrid_embedding_" + dataset + ".log"
    dictConfig(logging_config)

    # Create heuristic objects
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

    # Classifier
    classifier = HybridClassifier(heuristics=heuristic_list, dataset_db_name=dataset_db_name,
                                  dataset_split=dataset_split, annoy_metric=annoy_metric,
                                  bert_config_file=bert_config_file, init_checkpoint=init_checkpoint,
                                  vocab_file=vocab_file, seq_len=seq_len, split_table_name=split_table_name,
                                  skip_trivial_samples=skip_trivial_samples, prefill_symspell=True,
                                  batch_size=batch_size, layer_indexes=layer_indexes,
                                  use_one_hot_embeddings=use_one_hot_embeddings, do_lower_case=do_lower_case,
                                  annoy_index_path=annoy_index_path, num_trees=num_trees,
                                  annoy_output_dir=annoy_output_dir, distance_allowance=bert_distance_allowance)

    if entity_synonyms is None:
        print(classifier.classify(mentions=mention, sentence=sentence))
    else:
        output = classifier.get_potential_synonyms(entity=entity_synonyms,
                                                   distance_threshold=entity_synonyms_distance_threshold)
        for mention, distances in output.items():
            print("Mention: %s | Avg. distance: %.2f" % (mention, np.average(distances['distances'])))
            print("Entity: %s | Synonym: %s | Min. dist.: %.2f | Sentences: %s || NN-Sentences: %s" % (entity_synonyms, mention, np.min(distances['distances']), distances['sentences'], distances['nn_sentences']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classifier', nargs='?', type=str, default='rule', choices=['bert', 'rule', 'hybrid'])
    parser.add_argument('--entity_synonyms', nargs='*', type=str, default=None,
                        help="Enter an entity for which a ranked list of synonyms should be returned. If this "
                             "parameter is set, the --mention and --sentence parameter will be ignored.")
    parser.add_argument('--entity_synonyms_distance_threshold', nargs='?', type=float, default=0.85,
                        help="Enter a maximum distance threshold value that is used to filter out potential"
                             "synonyms/mentions if the --entity_synonyms parameter is set."
                             "Everything with a higher distance value is removed from the results.")
    parser.add_argument('--mention', nargs='*', default=['[NIL]'],
                        help="Enter a mention for which a single entity should be suggested.")
    parser.add_argument('--sentence', nargs='*', type=str, default=['[NIL]'],
                        help="Enter a sentence for which a) potential mentions will be identified and fitting entities "
                             "will be returned or b) if the --mention parameter is set with a mention that can be "
                             "found in the provided sentence, an entity will be returned as classification result "
                             "for the provided mention based on the context given with the sentence.")
    args = parser.parse_args()

    if len(args.mention) > 1:
        args.mention = ' '.join(args.mention)
    else:
        args.mention = args.mention[0]

    if len(args.sentence) > 1:
        args.sentence = ' '.join(args.sentence)
    else:
        args.sentence = args.sentence[0]

    if args.entity_synonyms is not None and len(args.entity_synonyms) > 1:
        args.entity_synonyms = ' '.join(args.entity_synonyms)
    elif args.entity_synonyms is not None:
        args.entity_synonyms = args.entity_synonyms[0]

    if args.classifier == 'bert':
        bert_embedding_classifier_main(args.mention, args.sentence, args.entity_synonyms, args.entity_synonyms_distance_threshold)
    elif args.classifier == 'rule':
        rule_classifier_main(args.mention, args.sentence, args.entity_synonyms, args.entity_synonyms_distance_threshold)
    elif args.classifier == 'hybrid':
        hybrid_classifier(args.mention, args.sentence, args.entity_synonyms, args.entity_synonyms_distance_threshold)
