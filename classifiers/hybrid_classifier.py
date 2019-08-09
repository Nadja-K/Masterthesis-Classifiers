from classifiers.classifier import Classifier
from classifiers.rule_classifier import RuleClassifier
from classifiers.bert_classifier import BertEmbeddingClassifier
from utils.heuristics import *
from typing import Union, Dict, List
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

    def _classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]", num_results: int=1) -> \
            Union[Dict[str, Dict[str, Union[float, int]]], List[Tuple[str, Dict[str, Dict[str, Union[float, int]]]]]]:
        assert sentence != "[NIL]", "The hybrid classifier requires at least a sentence in which potential " \
                                    "mentions can be identified for the classification."

        assert (self.rule_classifier._loaded_datasplit == self.bert_classifier._loaded_datasplit ==
                self._loaded_datasplit), "One of the classifiers has a different datasplit loaded"

        # If no mention has been provided, identify potential ones in the sentence.
        if mentions == "[NIL]":
            mentions = self._identify_potential_mentions(sentence)

        multi_mentions = isinstance(mentions, List)
        if multi_mentions is False:
            mentions = [mentions]

        all_suggestions = []
        case_2_mentions = {}
        case_3_mentions = []
        # Case 1: rule based finds exactly 1 entity, Rule-based only
        rule_suggestions = self.rule_classifier._classify(mentions, sentence)
        for (mention, suggestions) in rule_suggestions:
            if len(suggestions['suggestions']) == 1:
                all_suggestions.append((mention, suggestions))

            # Case 2: rule based finds > 1 entities, Rule-based + Bert-based
            # Save all mentions that fit case 2
            elif len(suggestions['suggestions']) > 1:
                case_2_mentions[mention] = suggestions

            # Case 3: rule based finds exactly 0 entities, Bert-based only
            # Save all mentions that fit case 3
            else:
                case_3_mentions.append(mention)

        # Case 2: rule based finds > 1 entities, Rule-based + Bert-based
        if len(case_2_mentions) > 0:
            # Do the classification of all case 2 mentions at once, then handle every mention by itself
            bert_suggestions = self.bert_classifier._classify(list(case_2_mentions.keys()), sentence, num_results=5)

            for (mention, bert_mention_suggestions) in bert_suggestions:
                rule_mention_suggestions = case_2_mentions[mention]

                # Prioritize entities that were found in both the rule-based classifier and the top 5 nearest neighbors
                # of the bert based classifier. Return the best entity of this intersection based on the bert distance.
                # Otherwise only rely on the bert entities.
                best_suggestion = ()
                for rule_suggestion in rule_mention_suggestions['suggestions']:
                    if rule_suggestion in bert_mention_suggestions['suggestions']:
                        if len(best_suggestion) > 0:
                            if bert_mention_suggestions['suggestions'][rule_suggestion] > best_suggestion[1]:
                                best_suggestion = (rule_suggestion, bert_mention_suggestions['suggestions'][rule_suggestion])
                        else:
                            best_suggestion = (rule_suggestion, bert_mention_suggestions['suggestions'][rule_suggestion])

                if len(best_suggestion) > 0:
                    all_suggestions.append((mention, {'suggestions': {best_suggestion[0]: best_suggestion[1]}}))
                else:
                    tmp = sorted(bert_mention_suggestions['suggestions'].items(), key=operator.itemgetter(1))[0]
                    tmp = {'suggestions': {tmp[0]: tmp[1]}}
                    all_suggestions.append((mention, tmp))

        # Case 3: rule based finds exactly 0 entities, Bert-based only
        if len(case_3_mentions) > 0:
            # Do the classification of all case 3 mentions at once, then handle every mention by itself
            bert_suggestions = self.bert_classifier._classify(case_3_mentions, sentence, num_results=1)

            for (mention, bert_mention_suggestions) in bert_suggestions:
                all_suggestions.append((mention, bert_mention_suggestions))

        if multi_mentions is False:
            return all_suggestions[0][1]
        else:
            return all_suggestions

    def classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]") -> \
            Union[Set[str], List[Tuple[str, Set[str]]]]:
        self._verify_data(self._loaded_datasplit)
        assert (self.rule_classifier._loaded_datasplit == self.bert_classifier._loaded_datasplit ==
                self._loaded_datasplit), "One of the classifiers has a different datasplit loaded."

        suggestions = self._classify(mentions, sentence)

        if isinstance(mentions, List) is False and mentions != "[NIL]":
            return set(suggestions['suggestions'].keys())
        else:
            res = []
            for (mention, mention_suggestions) in suggestions:
                res.append((mention, set(mention_suggestions['suggestions'].keys())))

            return res

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

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions',
                           empolis_mapping_path: str=None, empolis_distance_threshold: float=0.85):
        """
        Public method to evaluate a dataset.

        The empolis dataset is a bit different from the Wikipedia dataset. The distance threshold is
        only used for limiting entity suggestions of unknown mentions.
        For all mentions that are known to the empolis dataset, this threshold is not relevant, because for both the
        hybrid and the bert classifier, only exactly 1 entity is returned per sample. Therefore, it does not matter
        if a suggestion for which the classifier is unsure is removed or kept (wrong stays wrong).
        """
        assert num_results == 1, 'NUM_RESULTS should not be set for the hybrid classifier. The number of results is ' \
                                 'already chosen in an appropriate manner for the classifiers incorporated in this' \
                                 'hybrid approach. '

        self._verify_data(dataset_split)
        assert (self._loaded_datasplit == self.rule_classifier._loaded_datasplit ==
                self.bert_classifier._loaded_datasplit), 'The evaluation could not be performed because one ' \
                                                         'of the classifiers had a different dataset loaded. ' \
                                                         'Only run the evaluation on ' \
                                                         'its own without manual classification requests.'

        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode,
                                   empolis_mapping_path=empolis_mapping_path,
                                   empolis_distance_threshold=empolis_distance_threshold)

    def evaluate_potential_synonyms(self, empolis_mapping_path: str, distance_threshold: float=0.85):
        """
        Evaluate the classifiers ability to predict synonyms given an entity for the whole dataset.
        """
        # Fill the symspell dictionaries of all heuristics for all entities (or rather their appropiate version)
        self._verify_data(dataset_split=self._loaded_datasplit)
        assert (self._loaded_datasplit == self.rule_classifier._loaded_datasplit ==
                self.bert_classifier._loaded_datasplit), 'The evaluation could not be performed because one ' \
                                                         'of the classifiers had a different dataset loaded. ' \
                                                         'Only run the evaluation on ' \
                                                         'its own without manual classification requests.'

        # The actual evaluation process
        super().evaluate_potential_synonyms(empolis_mapping_path=empolis_mapping_path,
                                            distance_threshold=distance_threshold)
