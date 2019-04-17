from classifiers.classifier import Classifier


class EmbeddingClassifier(Classifier):
    def __init__(self):
        super().__init__()

    def classify(self):
        pass

    # FIXME: prepare the evaluation so that it is similar to the rule-based classifier and averages the results over the amount of equal mentions
    # e.g. Astro-Physik is a mention that appears in 100 sentences while astrophysics only appears once.
    # If we count every sentence for itself and our system is able to match Astro-Physik correctly but fails for astrophysics, it would still
    # end up with a high score. However, this is not what we want. We want to measure the average score per mention.
    # So: we calculate the performance for 1 sentence and later average the performance over the duplicate mentions.