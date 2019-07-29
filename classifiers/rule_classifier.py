from typing import Dict, Union

from classifiers.classifier import Classifier
from utils.heuristics import *


class RuleClassifier(Classifier):
    def __init__(self, heuristics: List[Heuristic], dataset_db_name: str, dataset_split: str,
                 split_table_name: str='splits', skip_trivial_samples: bool = False, prefill_symspell: bool = True,
                 query_data=None, context_data=None, entities=None, loaded_datasplit=None):
        super().__init__(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                         split_table_name=split_table_name, skip_trivial_samples=skip_trivial_samples,
                         load_context=False, query_data=query_data, context_data=context_data,
                         entities=entities, loaded_datasplit=loaded_datasplit)
        self._heuristics = heuristics
        self._symspell_loaded_datasplit = None

        # Fill the symspell dictionaries of each heuristic with the data of the train split
        # The flag is used in order to re-fill the dictionaries if a different split needs to be used.
        if prefill_symspell:
            print("Filling the symspell dictionaries for the %s split. This might take a while." % dataset_split)
            self._fill_symspell_dictionaries(dataset_split)
            self._symspell_loaded_datasplit = dataset_split

    def _fill_symspell_dictionaries(self, dataset_split: str):
        """
        Symspell is used to speed up the matching of a given word with a set of entities (and potentially their
        variations based on the heuristics used in this classifier).
        Each heuristic has its own sym_spell checker with a separate dictionary.
        Furthermore, each heuristic has a mapping dictionary to map a refactored form of an entity to the original.
        It should be noted, that it is entirely possible for a refactored form to be mapped to multiple entities.
        """
        if self._symspell_loaded_datasplit != dataset_split:
            if self._loaded_datasplit != dataset_split:
                print("The %s data hasn't been loaded yet. Doing this now, this will overwrite any previously loaded "
                      "data." % dataset_split)
                self._query_data, self._context_data, self._entities, self._loaded_datasplit = \
                    self.load_datasplit(dataset_db_name=self._dataset_db_name, dataset_split=dataset_split,
                                        skip_trivial_samples=True, load_context=False)
            print("The symspell dictionaries have not been filled with the %s data. Doing this now. This might take "
                  "a while." % dataset_split)

            # Make sure the sym spell dictionaries are new
            for heuristic in self._heuristics:
                heuristic.initialize_sym_speller()

            for entity in self._entities:
                # We want to refactor the already refactored entity further with every rule (with some exceptions)
                previous_refactored_entity = entity
                for heuristic in self._heuristics:
                    # Apply the heuristic to the entity and add it to the symspell dictionary
                    previous_refactored_entity = heuristic.add_dictionary_entity(previous_refactored_entity, entity)
            self._symspell_loaded_datasplit = dataset_split

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions', empolis_mapping_path: str=None):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        # Fill the symspell dictionaries of all heuristics for all entities (or rather their appropiate version)
        self._fill_symspell_dictionaries(dataset_split=dataset_split)

        # The actual evaluation process
        assert num_results == 1, 'NUM_RESULTS should not be set for the rule-based classifier. Instead all results ' \
                                 'with the same distance are returned for this classifier.'
        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode, empolis_mapping_path=empolis_mapping_path)

    def _classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]", num_results: int=1) -> \
            Union[Dict[str, Dict[str, Union[float, int]]], List[Tuple[str, Dict[str, Dict[str, Union[float, int]]]]]]:
        """
        Internal classify method that collects raw results that might be interesting for statistics.
        """
        assert not (mentions == "[NIL]" and sentence == "[NIL]"), "The rule-based classifier needs at least one mention" \
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
            best_results = {'refactored_mention': '', 'suggestions': {}, 'heuristic': None}

            # We want to refactor the already refactored string further with every rule (with some exceptions)
            previous_refactored_mention = mention
            min_distance = 99999
            for heuristic in self._heuristics:
                suggestions, previous_refactored_mention = heuristic.lookup(previous_refactored_mention,
                                                                            original_mention=mention)
                # All returned suggestions have the same edit distance, so if the distance is lower than the current
                # best result, overwrite it with the new suggestions
                if len(suggestions) > 0 and suggestions[0].distance < min_distance:
                    best_results['refactored_mention'] = previous_refactored_mention
                    best_results['heuristic'] = heuristic.name()
                    best_results['suggestions'] = {}
                    for suggestion in suggestions:
                        if suggestion.distance < min_distance:
                            min_distance = suggestion.distance

                        for reference_entity in suggestion.reference_entities:
                            best_results['suggestions'][reference_entity] = suggestion.distance

                # If the distance is already perfect, return the result here
                if min_distance == 0.0:
                    break

            if multi_mentions is False:
                return best_results
            all_suggestions.append((mention, best_results))

        return all_suggestions

    def classify(self, mentions: Union[str, List[str]] = "[NIL]", sentence: str = "[NIL]") -> Union[Set[str], List[Tuple[str, Set[str]]]]:
        """
        Public classify method that users can use to classify a given string based on the defined split.
        If the symspell dictionaries have not been filled yet or have been filled with a different split, they will be
        refilled first. This might take a while depending on the size of the dataset.

        Note: the entities of the split will be used to fill the dictionaries.
        """
        # Fill the symspell dictionaries of all heuristics for all entities (or rather their appropriate version)
        self._fill_symspell_dictionaries(dataset_split=self._loaded_datasplit)

        suggestions = self._classify(mentions, sentence)

        if isinstance(mentions, List) is False and mentions != "[NIL]":
            return set(suggestions['suggestions'].keys())
        else:
            res = []
            for (mention, mention_suggestions) in suggestions:
                res.append((mention, set(mention_suggestions['suggestions'].keys())))

            return res
