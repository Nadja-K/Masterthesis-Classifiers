import logging
import os

from classifiers.classifier import Classifier
from utils.annoy_index import Sent2VecIndexer
from typing import Set, Tuple, Dict, Union, List

log = logging.getLogger(__name__)


class TokenLevelEmbeddingClassifier(Classifier):
    def __init__(self, dataset_db_name: str, dataset_split: str, embedding_model_path: str, annoy_metric: str,
                 split_table_name: str='splits', skip_trivial_samples: bool = False, annoy_index_path: str=None,
                 num_trees: int=30, annoy_output_dir: str='', use_compound_splitting: bool=True,
                 compound_splitting_threshold: float=0.5, distance_allowance: float=0.05):
        super().__init__(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                         split_table_name=split_table_name,
                         skip_trivial_samples=skip_trivial_samples, load_context=False)

        self._embedding_model_path = embedding_model_path
        self._annoy_metric = annoy_metric
        self._use_compound_splitting = use_compound_splitting
        self._compound_splitting_threshold = compound_splitting_threshold
        self._annoy_index_path = annoy_index_path
        self._annoy_output_dir = annoy_output_dir
        self._dataset_db_name = dataset_db_name
        self._num_trees = num_trees
        self._distance_allowance = distance_allowance
        self._annoy_loaded_datasplit = None
        self._index = None

        self._fill_index(dataset_split)

    def _fill_index(self, dataset_split: str):
        # Create (or load) annoy index (If no data has been loaded or if new data needs to be loaded do this here)
        if self._annoy_loaded_datasplit != dataset_split:
            assert self._annoy_loaded_datasplit is None, "Annoy stores data in the RAM, creating a new index in the " \
                                                         "same session can cause problems with the indexed data. As " \
                                                         "a result, this feature is not supported currently. " \
                                                         "Only load one split per session."

            if dataset_split != self._loaded_datasplit:
                print("The %s data hasn't been loaded yet. Doing this now, this will overwrite any previously loaded "
                      "data." % dataset_split)
                self._query_data, self._context_data, self._entities, self._loaded_datasplit = \
                    self.load_datasplit(dataset_db_name=self._dataset_db_name, dataset_split=dataset_split,
                                        skip_trivial_samples=True, load_context=False)

            # If a new index has to be created, make sure the old one is unloaded
            if self._index is not None:
                self._index.close_index()
            print("The annoy index has not been filled with the %s data. Doing this now. This might take "
                  "a while." % dataset_split)

            # Create (or load) the annoy index
            self._index = Sent2VecIndexer(self._embedding_model_path, self._annoy_metric, self._use_compound_splitting,
                                          self._compound_splitting_threshold)
            if self._annoy_index_path is None:
                log.info("No annoy index file has been provided, creating new index now.")
                output_path = os.path.join(self._annoy_output_dir, "%s_%s" % (
                    self._dataset_db_name.split(os.sep)[-1].split(".")[0], dataset_split))
                self._index.create_entity_index(self._context_data, output_path, self._num_trees)
                self._output_path = output_path
            else:
                log.info("Loading provided annoy index.")
                self._index.load_entity_index(self._annoy_index_path)
                self._output_path = self._annoy_index_path

            self._annoy_loaded_datasplit = dataset_split

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions', empolis_mapping_path: str=None):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        # Make sure the correct data is loaded
        self._fill_index(dataset_split)

        # The actual evaluation process
        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode, empolis_mapping_path=empolis_mapping_path)

    def _classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]", num_results: int=1) -> \
            Union[Dict[str, Dict[str, Union[float, int]]], List[Tuple[str, Dict[str, Dict[str, Union[float, int]]]]]]:
        assert not (mentions == "[NIL]" and sentence == "[NIL]"), "The token-level classifier needs at least one mention" \
                                                                  " for the classification. Otherwise provide a " \
                                                                  "sentence in which possible mentions can be identified."

        # If no mention has been provided, identify potential ones in the sentence.
        if mentions == "[NIL]":
            mentions = self._identify_potential_mentions(sentence)

        multi_mentions = isinstance(mentions, List)
        if multi_mentions is False:
            mentions = [mentions]

        all_suggestions = []
        for mention in mentions:
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

            if multi_mentions is False:
                return top_suggestions
            all_suggestions.append((mention, top_suggestions))

        return all_suggestions

    def classify(self, mentions: Union[str, List[str]] = "[NIL]", sentence: str = "[NIL]") \
            -> Union[Set[str], List[Tuple[str, Set[str]]]]:
        # Make sure the correct data is loaded
        self._fill_index(self._loaded_datasplit)

        suggestions = self._classify(mentions, sentence, num_results=1)

        if isinstance(mentions, List) is False and mentions != "[NIL]":
            return set(suggestions['suggestions'].keys())
        else:
            res = []
            for (mention, mention_suggestions) in suggestions:
                res.append((mention, set(mention_suggestions['suggestions'].keys())))

            return res


