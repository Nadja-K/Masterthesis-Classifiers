import configparser

from rule_classifier import RuleClassifier


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    dataset_db_name = config['DATASET'].get('DATASET_DATABASE_NAME', '')
    use_negative_samples = config['DATASET'].getboolean('USE_NEGATIVE_SAMPLES', False)
    skip_trivial_samples = config['DATASET'].getboolean('SKIP_TRIVIAL_SAMPLES', False)
    classifier_threshold = config['CLASSIFIER'].getfloat('THRESHOLD', 1.0)

    classifier = RuleClassifier(dataset_db_name, load_negative_samples=use_negative_samples, skip_trivial_samples=skip_trivial_samples)
    classifier.classify_datasplit('train', threshold=classifier_threshold)


if __name__ == '__main__':
    main()
