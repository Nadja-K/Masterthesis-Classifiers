import configparser

from classifiers.rule_classifier import RuleClassifier
from classifiers.rule_classifier import HeuristicPunctuation, HeuristicStemming, HeuristicSort, HeuristicStopwords, \
    HeuristicAbbreviations


def main():
    config = configparser.ConfigParser()
    config.read("configs/config.ini")
    # config.read("configs/remote_config.ini")

    dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')
    skip_trivial_samples = config['DATASET'].getboolean('SKIP_TRIVIAL_SAMPLES', False)

    # Create heuristic objects
    punctuation_heuristic = HeuristicPunctuation()
    stemming_heuristic = HeuristicStemming()
    stopword_heuristic = HeuristicStopwords()
    sort_heuristic = HeuristicSort()
    abbreviation_heuristic = HeuristicAbbreviations(0.1)

    # The order of the heuristics in this list matters because each heuristic will use the previous refactored string
    heuristic_list = [punctuation_heuristic, stemming_heuristic, stopword_heuristic, sort_heuristic,
                      abbreviation_heuristic]
    classifier = RuleClassifier(heuristic_list, dataset_db_name, skip_trivial_samples, False)
    classifier.evaluate_datasplit('train')
    # classifier.classify_datasplit('train', threshold=classifier_threshold)


if __name__ == '__main__':
    main()
