import configparser

from rule_classifier import RuleClassifier
from rule_classifier import HeuristicPunctuation, HeuristicStemming, HeuristicSort, HeuristicStopwords


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    # config.read("remote_config.ini")

    dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')
    skip_trivial_samples = config['DATASET'].getboolean('SKIP_TRIVIAL_SAMPLES', False)
    classifier_threshold = config['CLASSIFIER'].getfloat('THRESHOLD', 1.0)

    # FIXME: is the original_heuristic even necessary?
    punctuation_heuristic = HeuristicPunctuation()
    stemming_heuristic = HeuristicStemming()
    stopword_heuristic = HeuristicStopwords()
    sort_heuristic = HeuristicSort()

    # The order of the heuristics in this list matters because each heuristic will use the previous refactored string
    heuristic_list = [punctuation_heuristic, stemming_heuristic, stopword_heuristic, sort_heuristic]
    classifier = RuleClassifier(heuristic_list)
    classifier.load_datasets(dataset_db_name,
                            skip_trivial_samples=skip_trivial_samples)
    classifier.evaluate_datasplit('val')
    # classifier.classify_datasplit('train', threshold=classifier_threshold)


if __name__ == '__main__':
    main()
