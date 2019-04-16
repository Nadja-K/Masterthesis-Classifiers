import sys
import sqlite3
import datetime

from Levenshtein import ratio  # https://github.com/ztane/python-Levenshtein
from typing import Tuple, List, Dict, Set, Union
from symspellpy.symspellpy import Verbosity

from classifiers.classifier import Classifier
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
            # We want to refactor the already refactored entity further with every rule
            previous_refactored_entity = entity

            # FIXME: is it possible to combine it with _classify so that changes/limitations (e.g. the abbreviation one) don't have to be written twice (and possibly forgotten)
            # Maybe use the classify method but with an extra flag to disable the best_result calculation?
            for heuristic in self.heuristics:
                # For the abbreviation heuristic, use the original mention
                if heuristic.name() == 'abbreviations':
                # FIXME: not original mention but the one from the filtering out punctuation
                    refactored_entity = heuristic.refactor(entity)
                else:
                    refactored_entity = heuristic.refactor(previous_refactored_entity)
                previous_refactored_entity = refactored_entity

                # Save the refactored entity in the heuristic symspeller + the mapping to the untouched entity
                heuristic.sym_speller.create_dictionary_entry(refactored_entity, 1)
                if refactored_entity not in heuristic.rule_mapping:
                    heuristic.rule_mapping[refactored_entity] = {entity}
                else:
                    heuristic.rule_mapping[refactored_entity].update({entity})

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

        # Calculate micro precision, recall and f1-score
        self._calculate_fscore(eval_results, data)

        # Printing the results
        # for mention, res in eval_results.items():
        #     matched_entities = set()
        #     for suggestion in res['suggestions']:
        #         matched_entities.update(res['heuristic'].rule_mapping[suggestion])
        #
        #     print(mention, res['distance'], matched_entities)

    def _calculate_fscore(self, eval_results: Dict[str, Union[str, int, Set[str], Heuristic]], data: Dict[str, Set[str]]):
        TP = 0
        FP = 0
        FN = 0
        print("{:40}{:40}{:40}{:40}".format("Mention", "TP entities", "FP entities", "FN entities"))
        print("{:40}{:40}{:40}{:40}".format("-"*15,"-"*15,"-"*15,"-"*15))
        for mention, res in eval_results.items():
            matched_entities = set()
            for suggestion in res['suggestions']:
                matched_entities.update(res['heuristic'].rule_mapping[suggestion])

            TP_entities = data[mention] & matched_entities
            FN_entities = data[mention] - matched_entities
            FP_entities = matched_entities - data[mention]
            print("{:40}{:40}{:40}{:40}".format(mention, str(TP_entities), str(FP_entities), str(FN_entities)))

            TP += len(TP_entities)
            FP += len(FP_entities)
            FN += len(FN_entities)

        micro_precision = TP / (TP + FP)
        micro_recall = TP / (TP + FN)
        micro_f1_score = 2 * ((micro_precision * micro_recall) / (micro_precision + micro_recall))
        print(micro_precision, micro_recall, micro_f1_score)

    def _ratio(self, s1: str, s2: str, ldist: int) -> float:
        """
        Calculate a simple ratio between two strings based on their length and levenshtein distance.
        """
        len_sum = len(s1) + len(s2)
        return (len_sum - ldist) / len_sum

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
            entities = res['heuristic'].rule_mapping[suggestion]
            for entity in entities:
                ratio = self._ratio(res['refactored_mention'], suggestion, res['distance'])
                matched_entities.add((entity, ratio))

        return matched_entities

    def _classify(self, mention: str) -> Dict[str, Union[str, int, Set[str], Heuristic]]:
        """
        Internal classify method that collects raw results that might be interesting for statistics.
        """
        best_results = {'distance': 99999, 'suggestions': {}, 'heuristic': None}

        previous_refactored_mention = mention
        for heuristic in self.heuristics:
            # For the abbreviation heuristic, use the original mention
            if heuristic.name() == 'abbreviations':
                # FIXME: not original mention but the one from the filtering out punctuation
                refactored_mention = heuristic.refactor(mention)
                print(mention, refactored_mention)
            else:
                refactored_mention = heuristic.refactor(previous_refactored_mention)
            previous_refactored_mention = refactored_mention

            suggestions = heuristic.sym_speller.lookup(refactored_mention, Verbosity.CLOSEST)
            for suggestion in suggestions:
                if suggestion.distance <= best_results['distance']:
                    if suggestion.distance < best_results['distance']:
                        best_results['refactored_mention'] = refactored_mention
                        best_results['suggestions'] = {suggestion.term}
                        best_results['distance'] = suggestion.distance
                        best_results['heuristic'] = heuristic

                    # If the current heuristic is a different one from the best one and did NOT improve the
                    # similarity, ignore it.
                    # Only keep the results from the heuristic that FIRST achieved the shortest distance.
                    elif best_results['heuristic'].name() == heuristic.name():
                        best_results['suggestions'].update({suggestion.term})

        return best_results

    # # FIXME: move to heuristics.py
    # def _heuristic_abbreviations(self, s1: str, s2: str) -> Tuple[str, str]:
    #     if len(s1) > len(s2):
    #         # Case: s2 might be the abbreviation
    #         return ''.join([s[:1] for s in s1.split(" ")]), s2
    #     else:
    #         # Case: s1 might be the abbreviation
    #         return s1, ''.join([s[:1] for s in s2.split(" ")])
    #
    #
    # # FIXME: remove
    # def compute_similarity(self, mention: str, reference_entity: str) -> Tuple[float, str, str]:
    #     """
    #     Decide if the string mention is identical to the string reference_entity or not.
    #     Example: GB and Großbritannien
    #     I use several heuristics to alter the two strings (removing punctuation, lowercasing, stemming, ...).
    #     After every heuristic, I calculate the similarity between the two altered strings.
    #     The highest similarity value is returned.
    #
    #     :param mention:
    #     :param reference_entity:
    #     :return:
    #     """
    #     # Initialize the highest_sim value
    #     highest_sim = (ratio(mention, reference_entity), mention, reference_entity)
    #     tmp_sim = highest_sim[0]
    #
    #     # Heuristic: remove punctuation in general
    #     tmp1, tmp2 = self._heuristic_punctuation(highest_sim[1], highest_sim[2])
    #     highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)
    #
    #     # Heuristic: stemming + lowercasing
    #     tmp1, tmp2 = self._heuristic_stemming(highest_sim[1], highest_sim[2])
    #     highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)
    #
    #     # Heuristic: remove stopwords
    #     tmp1, tmp2 = self._heuristic_remove_stopwords(highest_sim[1], highest_sim[2])
    #     highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)
    #
    #     # Heuristic: switch words (example: kenyon dorothy vs dorothy kenyon)
    #     tmp1, tmp2 = self._heuristic_sort_words(highest_sim[1], highest_sim[2])
    #     highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)
    #
    #     # Heuristic: word Splitter + keep the first letter of each word
    #     # FIXME muss ich natürlich anpassen wenn die regel nur noch auf 1 wort angewendet wird (dann kein vergleich ob mention oder entity die potentielle abkürzung ist, in dem fall einfach davon ausgehen, dass das wort die abkürzung ist)
    #     # FIXME für den Fall mention='GB' hieße das aber auch, dass wir die mention NICHT vorher in eine abkürzung umwandeln dürfen, wir müssen erstmal davon ausgehen dass unsere mention bereits die abkürzung ist und alle entities in abkürzungen umwandeln und so rausfinden, welche entity korrekt ist
    #     tmp1, tmp2 = self._heuristic_abbreviations(highest_sim[1], highest_sim[2])
    #     highest_sim_tmp = self._check_similarity(tmp1, tmp2, highest_sim)
    #     highest_sim = (highest_sim_tmp[0], highest_sim[1], highest_sim[2])
    #
    #     # FIXME: Heuristic: Compound Splitter u. 1 Buchstaben jeweils behalten
    #     # Note: incorporate into the above heuristic somehow?
    #     # Note2: definitely don't use the returned string from the above heuristic as input for this one
    #
    #     # Return a 'similarity' value (percentage) of the two strings/entities based on real minimal edit distance
    #     return highest_sim
