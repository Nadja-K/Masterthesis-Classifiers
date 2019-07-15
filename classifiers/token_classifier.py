import logging
import os

from classifiers.classifier import Classifier
from utils.annoy_index import Sent2VecIndexer
from typing import Set, Tuple, Dict, Union

log = logging.getLogger(__name__)


class TokenLevelEmbeddingClassifier(Classifier):
    def __init__(self, dataset_db_name: str, dataset_split: str, embedding_model_path: str, annoy_metric: str,
                 split_table_name: str='splits', skip_trivial_samples: bool = False, annoy_index_path: str=None,
                 num_trees: int=30, annoy_output_dir: str='', use_compound_splitting: bool=True,
                 compound_splitting_threshold: float=0.5, distance_allowance: float=0.05):
        super().__init__(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                         split_table_name=split_table_name,
                         skip_trivial_samples=skip_trivial_samples, load_context=False)

        self._distance_allowance = distance_allowance
        # Create (or load) the annoy index
        self._index = Sent2VecIndexer(embedding_model_path, annoy_metric, use_compound_splitting,
                                      compound_splitting_threshold)
        if annoy_index_path is None:
            log.info("No annoy index file has been provided, creating new index now.")
            output_path = os.path.join(annoy_output_dir, "%s_%s" % (dataset_db_name.split(os.sep)[-1].split(".")[0],
                                                                    dataset_split))
            self._index.create_entity_index(self._context_data, output_path, num_trees)
        else:
            log.info("Loading provided annoy index.")
            self._index.load_entity_index(annoy_index_path)

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions'):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        # The actual evaluation process
        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode)

    def _classify(self, mention: str, sentence: str = "", num_results: int=1) -> Dict[str, Dict[str, Union[float, int]]]:
        # Some minor refactoring before nearest neighbours are looked  up
        mention = str(mention)
        mention = mention.replace("-", " ").replace("(", " ").replace(")", " ").replace("_", " ")
        suggestions = self._index.get_nns_by_phrase(mention, sentence="", num_nn=num_results)

        top_suggestions = {'suggestions': {}}
        if len(suggestions) > 0:
            min_distance = suggestions[0][1]
            for tuple in suggestions:
                if self._distance_allowance is not None:
                    if tuple[1] <= (min_distance + self._distance_allowance):
                        top_suggestions['suggestions'][tuple[0]] = tuple[1]
                else:
                    top_suggestions['suggestions'][tuple[0]] = tuple[1]

        return top_suggestions

    def classify(self, mention: str, sentence: str = "") -> Set[Tuple[str, float, str]]:
        mention = str(mention)
        suggestions = self._index.get_nns_by_phrase(mention, sentence="", num_nn=1)
        if len(suggestions) > 0:
            min_distance = suggestions[0][1]
            # We want all tuples that have the smallest distance of the result.
            return set([tuple for tuple in suggestions if tuple[1] == min_distance])
        else:
            return set([])