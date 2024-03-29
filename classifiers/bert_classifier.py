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

        self._bert_config_file = bert_config_file
        self._init_checkpoint = init_checkpoint
        self._vocab_file = vocab_file
        self._seq_len = seq_len
        self._batch_size = batch_size
        self._layer_indexes = layer_indexes
        self._use_one_hot_embeddings = use_one_hot_embeddings
        self._do_lower_case = do_lower_case
        self._metric = annoy_metric
        self._num_trees = num_trees
        self._annoy_index_path = annoy_index_path
        self._annoy_output_dir = annoy_output_dir
        self._dataset_db_name = dataset_db_name
        self._annoy_loaded_datasplit = None
        self._index = None

        # Create (or load) annoy index
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
                self._index.close_session()
            print("The annoy index has not been filled with the %s data. Doing this now. This might take "
                  "a while." % dataset_split)

            self._index = BertIndexer(bert_config_file=self._bert_config_file, init_checkpoint=self._init_checkpoint,
                                      vocab_file=self._vocab_file, seq_len=self._seq_len, batch_size=self._batch_size,
                                      layer_indexes=self._layer_indexes,
                                      use_one_hot_embeddings=self._use_one_hot_embeddings,
                                      do_lower_case=self._do_lower_case, metric=self._metric)

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

    def close_session(self):
        self._index.close_session()

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions',
                           empolis_mapping_path: str=None, empolis_distance_threshold: float=0.85):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        # Make sure the correct data is loaded
        self._fill_index(dataset_split)

        # The actual evaluation process
        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode,
                                   empolis_mapping_path=empolis_mapping_path,
                                   empolis_distance_threshold=empolis_distance_threshold)

    def _get_potential_synonyms(self, distance_threshold=0.85):
        """
        Identify potential synonyms in all query sentences and return a dictionary for every entity that is known
        to the classifier with a ranked list of potential synonyms.
        """
        # Fill the symspell dictionaries of all heuristics for all entities (or rather their appropiate version)
        self._fill_index(dataset_split=self._loaded_datasplit)

        return super()._get_potential_synonyms(distance_threshold=distance_threshold)

    def _classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]", num_results: int=1) -> \
            Union[Dict[str, Dict[str, Union[float, int]]], List[Tuple[str, Dict[str, Dict[str, Union[float, int]]]]]]:
        assert sentence != "[NIL]", "The BERT-based classifier requires at least a sentence in which potential " \
                                    "mentions can be identified for the classification."
        # If no mention has been provided, identify potential ones in the sentence.
        if mentions == "[NIL]":
            mentions = self._identify_potential_mentions(sentence)

        multi_mentions = isinstance(mentions, List)
        if multi_mentions is False:
            mentions = [mentions]

        # multiple mentions have been identified prior for the query sentence - only calculate the token embeddings
        # of the sentence once.
        token_embeddings, token_mapping = self._index.get_token_embeddings(sentence)

        all_suggestions = []
        for mention in mentions:
            # Create mention embedding
            mention = str(mention)
            emb = self._index.get_mention_embedding(mention, sentence, token_mapping, token_embeddings)

            # Get nns by vector
            suggestions = self._index.get_nns_by_vector(emb, num_nn=num_results)

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

            if multi_mentions is False:
                return top_suggestions
            all_suggestions.append((mention, top_suggestions))

        return all_suggestions

    def classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]", num_results: int=1) -> \
            Union[Set[str], List[Tuple[str, Set[str]]], Dict[str, float]]:
        assert sentence != "[NIL]", "The BERT-based classifier requires at least a sentence for the classification " \
                                    "process."

        # Make sure the correct data is loaded
        self._fill_index(self._loaded_datasplit)

        suggestions = self._classify(mentions, sentence, num_results=num_results)

        if isinstance(mentions, List) is False and mentions != "[NIL]":
            res = {}
            for suggested_entity, distance in suggestions['suggestions'].items():
                if suggested_entity not in res.keys() or distance < res[suggested_entity]:
                    res[suggested_entity] = distance

            return res
        else:
            res = []
            for (mention, mention_suggestions) in suggestions:
                res.append((mention, mention_suggestions['suggestions']))

            return res
