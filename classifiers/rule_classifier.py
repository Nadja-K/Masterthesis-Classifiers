import sys
import sqlite3
import datetime

from Levenshtein import ratio  # https://github.com/ztane/python-Levenshtein
from typing import Tuple, List, Dict, Set, Union
from symspellpy.symspellpy import Verbosity, SuggestItem

from classifiers.classifier import Classifier
from eval.evaluation import RuleEvaluator, Evaluator
from heuristics.heuristics import *

epsilon = sys.float_info.epsilon


class RuleClassifier(Classifier):
    def __init__(self, heuristics: List[Heuristic], dataset_db_name: str, dataset_split: str,
                 skip_trivial_samples: bool = False, prefill_symspell: bool = True):
        assert dataset_split in ['train', 'test', 'val']
        super().__init__()
        self._dataset_db_name = dataset_db_name

        # Load the specified datasplit
        super()._load_datasplit(dataset_db_name, dataset_split, skip_trivial_samples, False)
        self._heuristics = heuristics

        # Fill the symspell dictionaries of each heuristic with the data of the train split
        # The flag is used in order to re-fill the dictionaries if a different split needs to be used.
        if prefill_symspell:
            print("Filling the symspell dictionaries for the %s split. This might take a while." % dataset_split)
            self._fill_symspell_dictionaries()
            self._symspell_loaded_datasplit = dataset_split
        else:
            self._symspell_loaded_datasplit = None

    def _fill_symspell_dictionaries(self, dataset_split):
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
                self._load_datasplit(dataset_db_name=self._dataset_db_name, dataset_split=dataset_split,
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

    def evaluate_datasplit(self, dataset_split: str):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        assert dataset_split in ['train', 'test', 'val']

        # Fill the symspell dictionaries of all heuristics for all entities (or rather their appropiate version)
        self._fill_symspell_dictionaries(dataset_split=dataset_split)

        # FIXME move this part to the parent classifier class? If possible
        start = datetime.datetime.now()

        i = 0
        eval_results = {}
        for sample in self._data:
            # FIXME: remove this later, just for fast debugging rn
            # if i > 100:
            #     break
            # i += 1
            mention = sample['mention']
            entity = sample['entity_title']
            suggestions = self._classify(mention)

            if 'sentence' not in suggestions:
                suggestions['sentence'] = sample['sentence']

            if entity not in eval_results:
                eval_results[entity] = {}

            if mention not in eval_results[entity]:
                eval_results[entity][mention] = []

            eval_results[entity][mention].append(suggestions)

        end = datetime.datetime.now()
        print("Classification took: ", end - start)

        # Calculate some metrics
        eval = Evaluator(self._mention_entity_duplicate_count)
        eval.evaluate(eval_results)
        # macro, micro = eval.evaluate(eval_results, data)
        # print("\nMacro metrics:"
        #       "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % macro)
        # print("\nMicro metrics:"
        #       "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % micro)
        pass

    def _ratio(self, s1: str, s2: str, ldist: int) -> float:
        """
        Calculate a simple ratio between two strings based on their length and levenshtein distance.
        """
        len_sum = len(s1) + len(s2)
        return (len_sum - ldist) / len_sum

    def _classify(self, mention: str) -> Dict[str, Union[str, Set[str], int, Heuristic]]:
        """
        Internal classify method that collects raw results that might be interesting for statistics.
        """
        best_results = {'distance': 99999, 'refactored_mention': '', 'suggestions': set(), 'heuristic': None}

        # We want to refactor the already refactored string further with every rule (with some exceptions)
        previous_refactored_mention = mention
        for heuristic in self._heuristics:
            suggestions, previous_refactored_mention = heuristic.lookup(previous_refactored_mention,
                                                                        original_mention=mention)
            # All returned suggestions have the same edit distance, so if the distance is lower than the current best
            # result, overwrite it with the new suggestions
            if len(suggestions) > 0 and suggestions[0].distance < best_results['distance']:
                best_results['refactored_mention'] = previous_refactored_mention
                best_results['distance'] = suggestions[0].distance
                best_results['heuristic'] = heuristic.name()
                best_results['suggestions'] = set()
                for suggestion in suggestions:
                    best_results['suggestions'].update(suggestion.reference_entities)

            # If the distance is already perfect, return the result here
            if best_results['distance'] == 0.0:
                return best_results

        return best_results

    def classify(self, mention: str) -> Set[Tuple[str, float]]:
        """
        Public classify method that users can use to classify a given string based on the train split.
        If the symspell dictionaries have not been filled yet or have been filled with a different split, they will be
        refilled first. This might take a while depending on the size of the dataset.

        Note: the entities of the split will be used to fill the dictionaries.
        """
        self._fill_symspell_dictionaries(dataset_split='train')

        res = self._classify(mention)
        matched_entities = set()
        for suggestion in res['suggestions']:
            for entity in suggestion.reference_entities:
                ratio = self._ratio(res['refactored_mention'], suggestion.term, suggestion.distance)
                matched_entities.add((entity, ratio))

        return matched_entities
