import sys
import sqlite3
import datetime

from Levenshtein import ratio  # https://github.com/ztane/python-Levenshtein
from typing import Tuple, List, Dict, Set, Union
from symspellpy.symspellpy import Verbosity, SuggestItem

from classifiers.classifier import Classifier
from eval.evaluation import RuleEvaluator
from heuristics.heuristics import *

epsilon = sys.float_info.epsilon


class RuleClassifier(Classifier):
    def __init__(self, heuristics: List[Heuristic], dataset_db_name: str, skip_trivial_samples: bool = False,
                 prefill_symspell: bool = True):
        super().__init__()

        self.refactored_train_data = None
        self.refactored_test_data = None
        self.refactored_val_data = None

        # The datasets (or at least the train split) need always to be loaded because we need background knowledge
        # of which entities exist.
        self.load_datasets(dataset_db_name, skip_trivial_samples)
        self.heuristics = heuristics

        # Fill the symspell dictionaries of each heuristic with the data of the train split
        # The flag is used in order to re-fill the dictionaries if a different split needs to be used.
        if prefill_symspell:
            print("Filling the symspell dictionaries for the train split. This might take a while.")
            self._fill_symspell_dictionaries(self.train_entities)
            self._symspell_loaded_datasplit = 'train'
        else:
            self._symspell_loaded_datasplit = None

    def load_datasets(self, dataset_db_name: str, skip_trivial_samples: bool = False, load_context: bool = False):
        """
        This overwrited the load_dataset method from the parent class and refactors the loaded samples in such
        a way that a set of mentions per split is left with a reference to all entities that would be a positive match.
        """
        super().load_datasets(dataset_db_name, skip_trivial_samples, load_context)

        # The data loaded from the database is a list of samples, but we need the mentions and the entities they
        # refer to. So refactor the data into an easier format for this task.
        self.refactored_train_data = self._create_data_dict(self.train_data)
        self.refactored_test_data = self._create_data_dict(self.test_data)
        self.refactored_val_data = self._create_data_dict(self.val_data)

        # Some statistical information
        print("Found a total of %s unique mentions in the train split." % len(self.refactored_train_data.keys()))
        print("Found a total of %s unique mentions in the test split." % len(self.refactored_test_data.keys()))
        print("Found a total of %s unique mentions in the val split." % len(self.refactored_val_data.keys()))

    def _create_data_dict(self, data: List[sqlite3.Row]) -> Dict[str, Set[str]]:
        """
        The data returned from the DB is a list of Row objects.
        Each row object represents a sample in our dataset. However, for the rule-based classifier we
        are only interested in the mentions (and only one at each time).
        This function creates a dictionary of mentions from the dataset and remembers the entities they
        refer to (in theory it is possible that a mention refers to multiple entities, in such a case both
        would be a positive ground truth case).
        """
        data_dict = {}
        for sample in data:
            if str(sample['mention']) not in data_dict.keys():
                data_dict[str(sample['mention'])] = {sample['entity_title']}
            else:
                data_dict[str(sample['mention'])].update([sample['entity_title']])

        return data_dict

    def _fill_symspell_dictionaries(self, entities):
        """
        Symspell is used to speed up the matching of a given word with a set of entities (and potentially their
        variations based on the heuristics used in this classifier).
        Each heuristic has its own sym_spell checker with a separate dictionary.
        Furthermore, each heuristic has a mapping dictionary to map a refactored form of an entity to the original.
        It should be noted, that it is entirely possible for a refactored form to be mapped to multiple entities.
        """
        # Make sure the sym spell dictionaries are new
        for heuristic in self.heuristics:
            heuristic.initialize_sym_speller()

        for entity in entities:
            # We want to refactor the already refactored entity further with every rule (with some exceptions)
            previous_refactored_entity = entity
            for heuristic in self.heuristics:
                # Apply the heuristic to the entity and add it to the symspell dictionary
                previous_refactored_entity = heuristic.add_dictionary_entity(previous_refactored_entity, entity)

    def evaluate_datasplit(self, split: str):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        assert split in ['train', 'test', 'val']

        if split == 'train':
            data = self.refactored_train_data
            entities = self.train_entities
        elif split == 'test':
            data = self.refactored_test_data
            entities = self.test_entities
        else:
            data = self.refactored_val_data
            entities = self.val_entities

        # Fill the symspell dictionaries of all heuristics for all entities (or rather their appropiate version)
        if self._symspell_loaded_datasplit != split:
            print("A wrong data split has been identified for the symspell dictionaries. Filling the symspell "
                  "dictionaries for the %s split. This might take a while." % split)
            self._fill_symspell_dictionaries(entities)
            self._symspell_loaded_datasplit = split

        start = datetime.datetime.now()
        eval_results = {}
        for mention in data.keys():
            eval_results[mention] = self._classify(mention)
        end = datetime.datetime.now()
        print("Classification took: ", end - start)

        # Calculate precision, recall and f1-score
        eval = RuleEvaluator()
        macro, micro = eval.evaluate(eval_results, data)
        print("\nMacro metrics:"
              "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % macro)
        print("\nMicro metrics:"
              "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % micro)

    def _ratio(self, s1: str, s2: str, ldist: int) -> float:
        """
        Calculate a simple ratio between two strings based on their length and levenshtein distance.
        """
        len_sum = len(s1) + len(s2)
        return (len_sum - ldist) / len_sum

    def _classify(self, mention: str) -> Dict[str, Union[str, List[SuggestItem], int, Heuristic]]:
        """
        Internal classify method that collects raw results that might be interesting for statistics.
        """
        best_results = {'distance': 99999, 'refactored_mention': '', 'suggestions': {}, 'heuristic': None}

        # We want to refactor the already refactored string further with every rule (with some exceptions)
        previous_refactored_mention = mention
        for heuristic in self.heuristics:
            suggestions, previous_refactored_mention = heuristic.lookup(previous_refactored_mention,
                                                                        original_mention=mention)
            # All returned suggestions have the same edit distance, so if the distance is lower than the current best
            # result, overwrite it with the new suggestions
            if len(suggestions) > 0 and suggestions[0].distance < best_results['distance']:
                best_results['refactored_mention'] = previous_refactored_mention
                best_results['suggestions'] = suggestions
                best_results['distance'] = suggestions[0].distance
                best_results['heuristic'] = heuristic.name()

            # If the distance is already perfect, return the result here
            if best_results['distance'] == 1.0:
                return best_results

        return best_results

    def classify(self, mention: str) -> Set[Tuple[str, float]]:
        """
        Public classify method that users can use to classify a given string based on the train split.
        If the symspell dictionaries have not been filled yet or have been filled with a different split, they will be
        refilled first. This might take a while depending on the size of the dataset.

        Note: the entities of the split will be used to fill the dictionaries.
        """
        if self._symspell_loaded_datasplit != 'train':
            print("The symspell dictionaries have not been filled with the train split data. Doing this now. "
                  "This might take a while.")
            self._fill_symspell_dictionaries(self.train_entities)
            self._symspell_loaded_datasplit = 'train'

        res = self._classify(mention)
        matched_entities = set()
        for suggestion in res['suggestions']:
            for entity in suggestion.reference_entities:
                ratio = self._ratio(res['refactored_mention'], suggestion.term, suggestion.distance)
                matched_entities.add((entity, ratio))

        return matched_entities
