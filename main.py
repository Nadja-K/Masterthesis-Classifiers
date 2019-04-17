import configparser

from classifiers.rule_classifier import RuleClassifier
from classifiers.rule_classifier import HeuristicPunctuation, HeuristicStemming, HeuristicSort, HeuristicStopwords, \
    HeuristicAbbreviationsCompounds, HeuristicAbbreviationsSpaces, HeuristicOriginal, HeuristicBrackets, \
    HeuristicLowercasing


def main():
    config = configparser.ConfigParser()
    config.read("configs/config.ini")
    # config.read("configs/remote_config.ini")

    dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')
    skip_trivial_samples = config['DATASET'].getboolean('SKIP_TRIVIAL_SAMPLES', False)

    # Create heuristic objects
    original_heuristic = HeuristicOriginal()
    brackets_heuristic = HeuristicBrackets()
    punctuation_heuristic = HeuristicPunctuation()
    lowercasing_heuristic = HeuristicLowercasing()
    stemming_heuristic = HeuristicStemming()
    stopword_heuristic = HeuristicStopwords()
    sort_heuristic = HeuristicSort()
    abbreviation_compounds_heuristic = HeuristicAbbreviationsCompounds(0.1)
    abbreviation_spaces_heuristic = HeuristicAbbreviationsSpaces()

    # The order of the heuristics in this list matters because each heuristic will use the previous refactored string
    heuristic_list = [brackets_heuristic, punctuation_heuristic, lowercasing_heuristic, stemming_heuristic,
                      stopword_heuristic, sort_heuristic, abbreviation_compounds_heuristic,
                      abbreviation_spaces_heuristic]
    heuristic_list = [brackets_heuristic, punctuation_heuristic, lowercasing_heuristic, stemming_heuristic,
                      stopword_heuristic, sort_heuristic, abbreviation_compounds_heuristic,
                      abbreviation_spaces_heuristic]
    # heuristic_list = [original_heuristic]
    classifier = RuleClassifier(heuristic_list, dataset_db_name, skip_trivial_samples, False)
    classifier.evaluate_datasplit('train')


if __name__ == '__main__':
    main()
