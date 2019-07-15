import logging
import os

from classifiers.classifier import Classifier
from utils.annoy_index import BertIndexer
from typing import Set, Tuple, Dict, Union, List

log = logging.getLogger(__name__)


class BertEmbeddingClassifier(Classifier):
    def __init__(self, dataset_db_name: str, dataset_split: str, annoy_metric: str,
                 bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int, batch_size: int = 32,
                 layer_indexes: List[int] = [-1, -2, -3, -4], use_one_hot_embeddings: bool = False,
                 do_lower_case: bool = True, skip_trivial_samples: bool = False,
                 split_table_name: str='splits', annoy_index_path: str=None, num_trees: int=30,
                 annoy_output_dir: str='', distance_allowance: float=0.05, query_data=None,
                 context_data=None, entities=None, loaded_datasplit=None):
        super().__init__(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                         split_table_name=split_table_name,
                         skip_trivial_samples=skip_trivial_samples, load_context=False, query_data=query_data,
                         context_data=context_data, entities=entities, loaded_datasplit=loaded_datasplit)

        self._distance_allowance = distance_allowance
        assert self._entities == set([x['entity_title'] for x in self._context_data]
                                     ), "The query and context data is not sharing the same entities."

        # Create (or load) annoy index
        self._index = BertIndexer(bert_config_file=bert_config_file, init_checkpoint=init_checkpoint,
                                  vocab_file=vocab_file, seq_len=seq_len, batch_size=batch_size,
                                  layer_indexes=layer_indexes, use_one_hot_embeddings=use_one_hot_embeddings,
                                  do_lower_case=do_lower_case, metric=annoy_metric)

        if annoy_index_path is None:
            log.info("No annoy index file has been provided, creating new index now.")
            output_path = os.path.join(annoy_output_dir, "%s_%s" % (dataset_db_name.split(os.sep)[-1].split(".")[0],
                                                                    dataset_split))
            self._index.create_entity_index(self._context_data, output_path, num_trees)
        else:
            log.info("Loading provided annoy index.")
            self._index.load_entity_index(annoy_index_path)

    def close_session(self):
        self._index.close_session()

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions'):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        # The actual evaluation process
        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode)

    def _classify(self, mention: str, sentence: str, num_results: int=1) -> Dict[str, Dict[str, Union[float, int]]]:
        suggestions = self._index.get_nns_by_phrase(mention, sentence=sentence, num_nn=num_results)

        top_suggestions = {'suggestions': {}, 'nn_sentences': suggestions, 'query_sentence': sentence}
        if len(suggestions) > 0:
            min_distance = suggestions[0][1]
            for tuple in suggestions:
                if (((self._distance_allowance is not None) and (tuple[1] <= (min_distance + self._distance_allowance)))
                        or (self._distance_allowance is None)):
                    # If the entity is already in the top suggestions, only keep the lowest distance
                    if tuple[0] in top_suggestions['suggestions'] and tuple[1] < top_suggestions['suggestions'][tuple[0]]:
                        top_suggestions['suggestions'][tuple[0]] = tuple[1]
                    # Otherwise only add the result if the entity is not in the top suggestions yet
                    elif tuple[0] not in top_suggestions['suggestions']:
                        top_suggestions['suggestions'][tuple[0]] = tuple[1]

        return top_suggestions

    def classify(self, mention: str, sentence: str) -> Set[Tuple[str, float, str]]:
        suggestions = self._index.get_nns_by_phrase(mention, sentence=sentence, num_nn=1)
        min_distance = suggestions[0][1]

        return set([tuple for tuple in suggestions if tuple[1] == min_distance])