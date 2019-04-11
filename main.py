import configparser

from rule_classifier import RuleClassifier


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')

    classifier = RuleClassifier(dataset_db_name)
    classifier.classify_datasplit('val', threshold=1.0)


if __name__ == '__main__':
    main()
