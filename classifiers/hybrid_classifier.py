from classifiers.classifier import Classifier
from classifiers.rule_classifier import RuleClassifier
from classifiers.bert_classifier import BertEmbeddingClassifier
from utils.heuristics import *
import operator


class HybridClassifier(Classifier):
    def __init__(self, heuristics: List[Heuristic], dataset_db_name: str, dataset_split: str, annoy_metric: str,
                 bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int,
                 split_table_name: str='splits', skip_trivial_samples: bool = False, prefill_symspell: bool = True,
                 batch_size: int=32, layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True, annoy_index_path: str=None, num_trees: int=30, annoy_output_dir: str='',
                 distance_allowance: float=0.05):

        # Load the data ONCE here
        super().__init__(dataset_db_name=dataset_db_name, dataset_split=dataset_split, split_table_name=split_table_name,
                         skip_trivial_samples=skip_trivial_samples, load_context=False)

        # Make an instance of the rule classifier and give the loaded data to it
        self.rule_classifier = RuleClassifier(heuristics=heuristics, dataset_db_name=dataset_db_name,
                                              dataset_split=dataset_split, split_table_name=split_table_name,
                                              skip_trivial_samples=skip_trivial_samples,
                                              prefill_symspell=prefill_symspell, query_data=self._query_data,
                                              context_data=self._context_data, entities=self._entities,
                                              loaded_datasplit=self._loaded_datasplit)

        # Do the same for the bert classifier
        self.bert_classifier = BertEmbeddingClassifier(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                                                       annoy_metric=annoy_metric, bert_config_file=bert_config_file,
                                                       init_checkpoint=init_checkpoint, vocab_file=vocab_file,
                                                       seq_len=seq_len, batch_size=batch_size,
                                                       layer_indexes=layer_indexes,
                                                       use_one_hot_embeddings=use_one_hot_embeddings,
                                                       do_lower_case=do_lower_case,
                                                       skip_trivial_samples=skip_trivial_samples,
                                                       split_table_name=split_table_name,
                                                       annoy_index_path=annoy_index_path, num_trees=num_trees,
                                                       annoy_output_dir=annoy_output_dir,
                                                       distance_allowance=distance_allowance,
                                                       query_data=self._query_data, context_data=self._context_data,
                                                       entities=self._entities, loaded_datasplit=self._loaded_datasplit)

    def _classify(self, mention: str, sentence: str, num_results: int=1):
        assert (self.rule_classifier._loaded_datasplit == self.bert_classifier._loaded_datasplit ==
                self._loaded_datasplit), "One of the classifiers has a different datasplit loaded"

        # Case 1: rule based finds exactly 1 entity, Rule-based only
        rule_suggestions = self.rule_classifier._classify(mention, sentence)
        if len(rule_suggestions['suggestions']) == 1:
            return rule_suggestions

        # Case 2: rule based finds > 1 entities, Rule-based + Bert-based
        elif len(rule_suggestions['suggestions']) > 1:
            bert_suggestions = self.bert_classifier._classify(mention, sentence, num_results=5)

            # Prioritize entities that were found in both the rule-based classifier and the top 5 nearest neighbors
            # of the bert based classifier. Return the best entity of this intersection based on the bert distance.
            # Otherwise only rely on the bert entities.
            best_suggestion = ()
            for rule_suggestion in rule_suggestions['suggestions']:
                if rule_suggestion in bert_suggestions['suggestions']:
                    if len(best_suggestion) > 0:
                        if bert_suggestions['suggestions'][rule_suggestion] > best_suggestion[1]:
                            best_suggestion = (rule_suggestion, bert_suggestions['suggestions'][rule_suggestion])
                    else:
                        best_suggestion = (rule_suggestion, bert_suggestions['suggestions'][rule_suggestion])

            if len(best_suggestion) > 0:
                return {'suggestions': {best_suggestion[0]: best_suggestion[1]}}
            else:
                tmp = sorted(bert_suggestions['suggestions'].items(), key=operator.itemgetter(1))[0]
                tmp = {'suggestions': {tmp[0]: tmp[1]}}
                return tmp

        # Case 3: rule based finds exactly 0 entities, Bert-based only
        else:
            bert_suggestions = self.bert_classifier._classify(mention, sentence, num_results=1)
            return bert_suggestions

    def classify(self, mention: str, sentence: str):
        self._verify_data(self._loaded_datasplit)
        assert (self.rule_classifier._loaded_datasplit == self.bert_classifier._loaded_datasplit ==
                self._loaded_datasplit), "One of the classifiers has a different datasplit loaded"

        res = self._classify(mention, sentence)
        tmp = sorted(res['suggestions'].items(), key=operator.itemgetter(1))[0]
        return tmp[0]

    def _verify_data(self, dataset_split):
        # Check if the correct data has been loaded (for all classifiers used in this approach)
        if dataset_split != self._loaded_datasplit:
            print("The %s data hasn't been loaded yet. Doing this now, this will overwrite any previously loaded "
                  "data." % dataset_split)
            self._query_data, self._context_data, self._entities, self._loaded_datasplit = \
                self.load_datasplit(dataset_db_name=self._dataset_db_name, dataset_split=dataset_split,
                                    skip_trivial_samples=True, load_context=False)

            # Update the data of the two classifiers as well so they don't need to be reloaded as well
            self.rule_classifier.set_data(self._query_data, self._context_data, self._entities, self._loaded_datasplit)
            self.bert_classifier.set_data(self._query_data, self._context_data, self._entities, self._loaded_datasplit)

        # And make sure the respective indexing step has been performed
        self.rule_classifier._fill_symspell_dictionaries(dataset_split)
        self.bert_classifier._fill_index(dataset_split)

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions'):
        assert num_results == 1, 'NUM_RESULTS should not be set for the hybrid classifier. The number of results is ' \
                                 'already chosen in an appropriate manner for the classifiers incorporated in this' \
                                 'hybrid approach. '

        self._verify_data(dataset_split)
        assert (self._loaded_datasplit == 'val' and self.rule_classifier._loaded_datasplit == 'val' and
                self.bert_classifier._loaded_datasplit == 'val'), 'The evaluation could not be performed because one' \
                                                                  'of the classifiers had a different dataset loaded' \
                                                                  'than the "val" dataset. Only run the evaluation on' \
                                                                  'its own without manual classification requests.'

        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode)
