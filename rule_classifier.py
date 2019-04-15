import string
import sys
import sqlite3
import datetime
from abc import ABCMeta, abstractmethod

from classifier import Classifier
from Levenshtein import ratio  # https://github.com/ztane/python-Levenshtein
from nltk import SnowballStemmer
from nltk.corpus import stopwords
from typing import Tuple, List, Dict, Set
from symspellpy.symspellpy import SymSpell, Verbosity

epsilon = sys.float_info.epsilon


class Heuristic(metaclass=ABCMeta):
    def __init__(self, max_edit_distance_dictionary=7, prefix_length=8, count_threshold=1, compact_level=0):
        self.sym_speller = SymSpell(max_edit_distance_dictionary, prefix_length, count_threshold, compact_level)
        self.rule_mapping = {}

    @property
    @abstractmethod
    def name(self):
        return "original"

    @abstractmethod
    def refactor(self, s: str) -> str:
        return s


class HeuristicPunctuation(Heuristic):
    def name(self):
        return "punctuation"

    def refactor(self, s: str) -> str:
        return s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) \
               .replace(' ' * 4, ' ').replace(' ' * 3, ' ').replace(' ' * 2, ' ').strip()


class HeuristicStemming(Heuristic):
    def __init__(self):
        super().__init__()
        self.stemmer = SnowballStemmer('german')

    def name(self):
        return "stemming"

    def refactor(self, s: str) -> str:
        return " ".join([self.stemmer.stem(word) for word in s.split(" ")])


class HeuristicStopwords(Heuristic):
    def __init__(self):
        super().__init__()
        self.stop_words = stopwords.words('german')

    def name(self):
        return "stopwords"

    def refactor(self, s: str) -> str:
        return ' '.join([word for word in s.split(" ") if word not in self.stop_words])


class HeuristicSort(Heuristic):
    def name(self):
        return "sort"

    def refactor(self, s: str) -> str:
        return " ".join(sorted(s.split(" ")))


# FIXME: remaining heuristics


class RuleClassifier(Classifier):
    def __init__(self, heuristics: List[Heuristic]):
        super().__init__()

        self.refactored_train_data = None
        self.refactored_test_data = None
        self.refactored_val_data = None

        self.heuristics = heuristics

    def load_datasets(self, dataset_db_name: str, skip_trivial_samples: bool = False, load_context: bool = False):
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
        for entity in entities:
            # We want to refactor the already refactored entity further with every rule
            previous_refactored_entity = entity

            for heuristic in self.heuristics:
                refactored_entity = heuristic.refactor(previous_refactored_entity)
                previous_refactored_entity = refactored_entity

                # Save the refactored entity in the heuristic symspeller + the mapping to the untouched entity
                heuristic.sym_speller.create_dictionary_entry(refactored_entity, 1)
                if refactored_entity not in heuristic.rule_mapping:
                    heuristic.rule_mapping[refactored_entity] = {entity}
                else:
                    heuristic.rule_mapping[refactored_entity].update({entity})

    def evaluate_datasplit(self, split: str):
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
        self._fill_symspell_dictionaries(entities)

        # FIXME: hashing approach
        print("Start comparing")
        eval_results = {}
        start = datetime.datetime.now()
        for mention in data.keys():
            best_results = {'distance': 99999, 'suggestions': {}, 'heuristic': None}

            previous_refactored_mention = mention
            for heuristic in self.heuristics:
                refactored_mention = heuristic.refactor(previous_refactored_mention)
                previous_refactored_mention = refactored_mention

                suggestions = heuristic.sym_speller.lookup(refactored_mention, Verbosity.CLOSEST)
                for suggestion in suggestions:
                    if suggestion.distance <= best_results['distance']:
                        if suggestion.distance < best_results['distance']:
                            best_results['suggestions'] = {suggestion.term}
                            best_results['distance'] = suggestion.distance
                            best_results['heuristic'] = heuristic

                        # If the current heuristic is a different one from the best one and did NOT improve the
                        # similarity, ignore it.
                        # Only keep the results from the heuristic that FIRST achieved the shortest distance.
                        elif best_results['heuristic'].name() == heuristic.name():
                            best_results['suggestions'].update({suggestion.term})

            # print(mention, best_results)
            # for suggestion in best_results['suggestions']:
            #     print(mention, best_results['heuristic'].rule_mapping[suggestion])
            eval_results[mention] = best_results
        end = datetime.datetime.now()
        print(end-start)
        print("Comparing done")

        print(eval_results)
        # FIXME: calculate some sort of accuracy?

    def classify(self, mention: str, entities: Set[str]) -> Dict[str, float]:
        similarity_results = {}
        for entity in entities:
            print(mention, entity)
            similarity_results[entity] = self.compute_similarity(mention, entity)

        return similarity_results

    # def classify_datasplit(self, split: str, threshold: float = 0.5):
    #     assert split in ['train', 'test', 'val']
    #
    #     if split == 'train':
    #         data = self.train_data
    #     elif split == 'test':
    #         data = self.test_data
    #     else:
    #         data = self.val_data
    #
    #     true_positive_count = 0
    #     true_negative_count = 0
    #     false_positive_count = 0
    #     false_negative_count = 0
    #     print("{0: <30} {1: <30} {2: <30} {3: <30} {4: <30}".format("Similarity", "Refactored mention",
    #                                                                   "Refactored entity", "Original mention",
    #                                                                   "Original entity"))
    #     print("-"*150)
    #     for sample in data:
    #         mention = str(sample['mention'])
    #         reference_entity = str(sample['entity_title'])
    #         positive = bool(sample['positive'])
    #
    #         ratio, s1, s2 = self.classify(mention, reference_entity)
    #         if ratio >= threshold:
    #             if positive:
    #                 # print("TP\t{0: <30} {1: <30} {2: <30} {3: <30} {4: <30}".format(ratio, s1, s2, mention, reference_entity))
    #                 true_positive_count += 1
    #             else:
    #                 # print("FP\t{0: <30} {1: <30} {2: <30} {3: <30} {4: <30}".format(ratio, s1, s2, mention, reference_entity))
    #                 false_positive_count += 1
    #         else:
    #             if positive:
    #                 # print("FN\t{0: <30} {1: <30} {2: <30} {3: <30} {4: <30}".format(ratio, s1, s2, mention, reference_entity))
    #                 false_negative_count += 1
    #             else:
    #                 # print("TN\t{0: <30} {1: <30} {2: <30} {3: <30} {4: <30}".format(ratio, s1, s2, mention, reference_entity))
    #                 true_negative_count += 1
    #
    #     precision = true_positive_count / (true_positive_count + false_positive_count + epsilon) * 100
    #     recall = true_positive_count / (true_positive_count + false_negative_count + epsilon) * 100
    #     accuracy = (true_positive_count + true_negative_count) / len(data) * 100
    #     f_measure = 2 * (precision * recall) / (precision + recall + epsilon)
    #     print("\nTP: %s, TN: %s, FP: %s, FN: %s" % (true_positive_count, true_negative_count, false_positive_count, false_negative_count))
    #     print("Precision: %.2f%%, Recall: %.2f%%, Accuracy: %.2f%%, F_1-Measure: %.2f%%" % (precision, recall, accuracy, f_measure))
    #
    #     print("%s\n%s\n%s\n%s\n%.2f\n%.2f\n%.2f\n%.2f" % (true_positive_count, true_negative_count, false_positive_count, false_negative_count, precision, recall, accuracy, f_measure))

    def _remove_stopwords(self, s: str) -> str:
        words = s.split(" ")
        return ' '.join([word for word in words if word not in self.stop_words])

    def _heuristic_punctuation(self, s: str) -> str:
        return s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))\
            .replace(' ' * 4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()

    # def _heuristic_punctuation(self, s1: str, s2: str) -> Tuple[str, str]:
    #     def remove_punctuation(s):
    #         return s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace(' '*4, ' ')\
    #             .replace(' '*3, ' ').replace(' '*2, ' ').strip()
    #
    #     return remove_punctuation(s1), remove_punctuation(s2)

    def _heuristic_stemming(self, s1: str, s2: str) -> Tuple[str, str]:
        def stem_string_sequence(s):
            words = []
            s_words = s.split(" ")
            for word in s_words:
                words.append(self.stemmer.stem(word))
            return " ".join(words)

        return stem_string_sequence(s1), stem_string_sequence(s2)

    def _heuristic_abbreviations(self, s1: str, s2: str) -> Tuple[str, str]:
        if len(s1) > len(s2):
            # Case: s2 might be the abbreviation
            return ''.join([s[:1] for s in s1.split(" ")]), s2
        else:
            # Case: s1 might be the abbreviation
            return s1, ''.join([s[:1] for s in s2.split(" ")])

    def _heuristic_sort_words(self, s1: str, s2: str) -> Tuple[str, str]:
        """
        Idea: if two strings consist of the same words but in different order, they probably still have the same
        meaning. In this case, sort all words of both strings in alphabetical order and then return them like this.
        """
        s1_words = sorted(s1.split(" "))
        s2_words = sorted(s2.split(" "))

        return ' '.join(s1_words), ' '.join(s2_words)

    def _heuristic_remove_stopwords(self, s1: str, s2: str) -> Tuple[str, str]:
        return self._remove_stopwords(s1), self._remove_stopwords(s2)

    def _check_similarity(self, s1, s2, highest_sim):
        sim = ratio(s1, s2)
        if sim >= highest_sim[0]:
            return sim, s1, s2
        return highest_sim

    def compute_similarity(self, mention: str, reference_entity: str) -> Tuple[float, str, str]:
        """
        Decide if the string mention is identical to the string reference_entity or not.
        Example: GB and Großbritannien
        I use several heuristics to alter the two strings (removing punctuation, lowercasing, stemming, ...).
        After every heuristic, I calculate the similarity between the two altered strings.
        The highest similarity value is returned.

        :param mention:
        :param reference_entity:
        :return:
        """
        # Initialize the highest_sim value
        highest_sim = (ratio(mention, reference_entity), mention, reference_entity)
        tmp_sim = highest_sim[0]

        # Heuristic: remove punctuation in general
        tmp1, tmp2 = self._heuristic_punctuation(highest_sim[1], highest_sim[2])
        highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)

        # Heuristic: stemming + lowercasing
        tmp1, tmp2 = self._heuristic_stemming(highest_sim[1], highest_sim[2])
        highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)

        # Heuristic: remove stopwords
        tmp1, tmp2 = self._heuristic_remove_stopwords(highest_sim[1], highest_sim[2])
        highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)

        # Heuristic: switch words (example: kenyon dorothy vs dorothy kenyon)
        tmp1, tmp2 = self._heuristic_sort_words(highest_sim[1], highest_sim[2])
        highest_sim = self._check_similarity(tmp1, tmp2, highest_sim)

        # Heuristic: word Splitter + keep the first letter of each word
        # FIXME muss ich natürlich anpassen wenn die regel nur noch auf 1 wort angewendet wird (dann kein vergleich ob mention oder entity die potentielle abkürzung ist, in dem fall einfach davon ausgehen, dass das wort die abkürzung ist)
        # FIXME für den Fall mention='GB' hieße das aber auch, dass wir die mention NICHT vorher in eine abkürzung umwandeln dürfen, wir müssen erstmal davon ausgehen dass unsere mention bereits die abkürzung ist und alle entities in abkürzungen umwandeln und so rausfinden, welche entity korrekt ist
        tmp1, tmp2 = self._heuristic_abbreviations(highest_sim[1], highest_sim[2])
        highest_sim_tmp = self._check_similarity(tmp1, tmp2, highest_sim)
        highest_sim = (highest_sim_tmp[0], highest_sim[1], highest_sim[2])

        # FIXME: Heuristic: Compound Splitter u. 1 Buchstaben jeweils behalten
        # Note: incorporate into the above heuristic somehow?
        # Note2: definitely don't use the returned string from the above heuristic as input for this one

        # Return a 'similarity' value (percentage) of the two strings/entities based on real minimal edit distance
        return highest_sim
