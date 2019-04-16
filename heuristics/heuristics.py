from abc import ABCMeta, abstractmethod

from nltk import SnowballStemmer
from nltk.corpus import stopwords

from symspellpy.symspellpy import SymSpell

import string


class Heuristic(metaclass=ABCMeta):
    # FIXME: parameter auslagern, damit experimentieren am ende für accuracy
    def __init__(self, max_edit_distance_dictionary=5, prefix_length=10, count_threshold=1, compact_level=5):
        """
        Note:  lower max_edit_distance and higher prefix_length=2*max_edit_distance == faster
        """
        self.max_edit_distance_dictionary = max_edit_distance_dictionary
        self.prefix_length = prefix_length
        self.count_threshold = count_threshold
        self.compact_level = compact_level

        self.sym_speller = None
        self.rule_mapping = {}

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def refactor(self, s: str) -> str:
        pass

    def initialize_sym_speller(self):
        self.sym_speller = SymSpell(self.max_edit_distance_dictionary, self.prefix_length, self.count_threshold,
                                    self.compact_level)
        self.rule_mapping = {}


class HeuristicPunctuation(Heuristic):
    def name(self):
        return "punctuation"

    def refactor(self, s: str) -> str:
        s = str(s)
        return s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))\
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
