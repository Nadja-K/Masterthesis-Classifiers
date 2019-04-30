from classifiers.classifier import Classifier
from index.annoy_index import AnnoyIndexer


class TokenLevelEmbeddingClassifier(Classifier):
    def __init__(self, dataset_db_name: str, dataset_split: str):
        assert dataset_split in ['train', 'test', 'val']
        super().__init__()
        self._dataset_db_name = dataset_db_name

        # Load the specified datasplit
        super()._load_datasplit(dataset_db_name, dataset_split, False, False)

        # FIXME: Create (or load if possible) the annoy index

    def evaluate_datasplit(self, split: str, eval_mode: str='mentions'):
        pass

    def _classify(self, mention: str):
        pass

    def classify(self, mention: str):
        pass
