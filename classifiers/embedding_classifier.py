import logging
import os
import time

from classifiers.classifier import Classifier
from index.annoy_index import Sent2VecIndexer
from typing import Set, Tuple, Dict, Union

log = logging.getLogger(__name__)


class TokenLevelEmbeddingClassifier(Classifier):
    def __init__(self, dataset_db_name: str, dataset_split: str, embedding_model_path: str, annoy_metric: str,
                 skip_trivial_samples: bool = False, annoy_index_path: str=None, num_trees: int=30,
                 annoy_output_dir: str=''):
        assert dataset_split in ['train', 'test', 'val']
        super().__init__()
        self._dataset_db_name = dataset_db_name

        # Load the specified datasplit
        super()._load_datasplit(dataset_db_name, dataset_split, skip_trivial_samples=skip_trivial_samples,
                                load_context=False)

        # Create (or load) the annoy index
        self._index = Sent2VecIndexer(embedding_model_path, annoy_metric)
        if annoy_index_path is None:
            log.info("No annoy index file has been provided, creating new index now.")
            output_path = os.path.join(annoy_output_dir, "%s_%s" % (dataset_db_name.split(os.sep)[-1].split(".")[0],
                                                                    dataset_split))
            self._index.create_entity_index(self._entities, output_path, num_trees)
        else:
            log.info("Loading provided annoy index.")
            self._index.load_entity_index(annoy_index_path)

    def evaluate_datasplit(self, dataset_split: str, eval_mode: str='mentions'):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        assert dataset_split in ['train', 'test', 'val']

        # The actual evaluation process
        super().evaluate_datasplit(dataset_split, eval_mode=eval_mode)

    def _classify(self, mention: str) -> Dict[str, Union[str, Set[str], int]]:
        # Some minor refactoring before nearest neighbours are looked  up
        mention = str(mention)
        mention = mention.replace("-", " ").replace("(", " ").replace(")", " ")
        suggestions = self._index.get_nns_by_phrase(mention, 1)

        min_distance = 99999
        top_10_suggestions = set([])
        if len(suggestions) > 0:
            min_distance = suggestions[0][1]
            top_10_suggestions = set([tuple[0] for tuple in suggestions if tuple[1] == min_distance])

        result = {'distance': min_distance, 'suggestions': top_10_suggestions}
        return result

    def classify(self, mention: str) -> Set[Tuple[str, float]]:
        # Some minor refactoring before nearest neighbours are looked  up
        mention = str(mention)
        mention = mention.replace("-", " ").replace("(", " ").replace(")", " ")
        suggestions = self._index.get_nns_by_phrase(mention, 1)
        min_distance = suggestions[0][1]

        # We want all tuples that have the smallest distance of the result (but max. up to 10).
        return set([tuple for tuple in suggestions if tuple[1] == min_distance])
