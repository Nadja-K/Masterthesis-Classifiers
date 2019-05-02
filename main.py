import configparser
import time
import json
import logging
from configs.logging_config import logging_config
from logging.config import dictConfig

from classifiers.embedding_classifier import TokenLevelEmbeddingClassifier, BertEmbeddingClassifier
from classifiers.rule_classifier import RuleClassifier
from classifiers.rule_classifier import HeuristicPunctuation, HeuristicStemming, HeuristicSort, HeuristicStopwords, \
    HeuristicAbbreviationsCompounds, HeuristicAbbreviationsSpaces, HeuristicOriginal, HeuristicBrackets, \
    HeuristicLowercasing, HeuristicCorporateForms

# Logging
# logging.disable(logging.WARNING)

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
    # Logging
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[0] + "_token_level_embedding.log"
    dictConfig(logging_config)

    # Settings
    annoy_metric = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('ANNOY_METRIC', 'euclidean')
    num_trees = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getint('NUM_TREES', 30)
    annoy_index_path = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('ANNOY_INDEX_PATH', None)
    annoy_output_dir = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('ANNOY_OUTPUT_DIR', '')
    # FIXME other arguments

    # Classifier
    classifier = BertEmbeddingClassifier(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                                         split_table_name=split_table_name,
                                         annoy_metric=annoy_metric, num_trees=num_trees,
                                         annoy_index_path=annoy_index_path, annoy_output_dir=annoy_output_dir,
                                         skip_trivial_samples=skip_trivial_samples)
    start = time.time()
    classifier.evaluate_datasplit(dataset_split, eval_sentences=True, eval_mode=eval_mode)
    print("Evaluation took %s" % (time.time() - start))


def token_level_embedding_classifier_main():
    # Logging
    logging_config['handlers']['fileHandler']['filename'] = logging_config['handlers']['fileHandler'][
                                                                'filename'].split(".")[0] + "_token_level_embedding.log"
    dictConfig(logging_config)

    # Settings
    embedding_model_path = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('EMBEDDING_MODEL_PATH', None)
    annoy_metric = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('ANNOY_METRIC', 'euclidean')
    num_trees = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getint('NUM_TREES', 30)
    annoy_index_path = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('ANNOY_INDEX_PATH', None)
    annoy_output_dir = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].get('ANNOY_OUTPUT_DIR', '')
    use_compound_splitting = config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getboolean('USE_COMPOUND_SPLITTING', True)
    compound_splitting_threshold =config['EMBEDDINGCLASSIFIER_TOKENLEVEL'].getfloat('COMPOUND_SPLITTING_THRESHOLD', 0.5)

    # Classifier
    classifier = TokenLevelEmbeddingClassifier(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                                               split_table_name=split_table_name,
                                               embedding_model_path=embedding_model_path, annoy_metric=annoy_metric,
                                               num_trees=num_trees, annoy_index_path=annoy_index_path,
                                               annoy_output_dir=annoy_output_dir,
                                               skip_trivial_samples=skip_trivial_samples,
                                               use_compound_splitting=use_compound_splitting,
                                               compound_splitting_threshold=compound_splitting_threshold)
    start = time.time()
    classifier.evaluate_datasplit(dataset_split, eval_sentences=False, eval_mode=eval_mode)
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
                                                                       0.1)
    abbreviation_spaces_heuristic = HeuristicAbbreviationsSpaces(abbreviations_max_edit_distance_dictionary,
                                                                 prefix_length, count_threshold, compact_level)

    # The order of the heuristics in this list matters because each heuristic will use the previous refactored string
    heuristic_list = [brackets_heuristic, punctuation_heuristic, corporate_forms_heuristic, lowercasing_heuristic,
                      stemming_heuristic, stopword_heuristic, sort_heuristic, abbreviation_compounds_heuristic,
                      abbreviation_spaces_heuristic]
    # heuristic_list = [original_heuristic]

    # Classifier
    classifier = RuleClassifier(heuristic_list, dataset_db_name, dataset_split, split_table_name,
                                skip_trivial_samples, False)
    start = time.time()
    classifier.evaluate_datasplit(dataset_split, eval_sentences=False, eval_mode=eval_mode)
    print("Evaluation took %s" % (time.time() - start))


if __name__ == '__main__':
    # token_level_embedding_classifier_main()
    # bert_embedding_classifier_main()
    rule_classifier_main()
