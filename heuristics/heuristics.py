from abc import ABCMeta, abstractmethod

from nltk import SnowballStemmer
from nltk.corpus import stopwords
from typing import List

from symspellpy.symspellpy import SymSpell
from CharSplit import char_split

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


class HeuristicAbbreviations(Heuristic):
    def __init__(self, prob_threshold):
        super().__init__()
        assert prob_threshold > 0
        self._prop_threshold = prob_threshold

    def name(self):
        return "abbreviations"

    def _split(self, s: str) -> List[str]:
        """
        This method recursively splits an input string into its compounds based on a probability threshold.

        The compound splitter used in this function (CharSplit) only splits a string into two compounds.
        However, words can have far more relevant compounds. To solve this issue I recursively split the compounds
        into further compounds until they no longer satisfy the probability threshold.

        CharSplit has some other 'weaknesses' that are covered here.
        1) If the input string consists of multiple words separated by a space, CharSplit is unable to handle it very
           well. Usually the resulting probability is negative. Instead, I split the input string manually on spaces.
        2) The compound splitter capitalizes every word, but I want them lowercased.
        3) CharSplit returns various splits (sorted by a probability) but to keep it simple, I only take the first one
           into consideration
        """
        if " " in s:
            split = s.split(" ")
            probability = 1.0
        else:
            split_res = char_split.split_compound(s)[0]
            probability = split_res[0]
            split = split_res[1:]
        compounds = [split.strip().lower() for split in split]

        if probability >= self._prop_threshold:
            recursive_compounds = []
            for compound in compounds:
                recursive_compounds.extend(self._split(compound))
            return recursive_compounds
        else:
            return [s]

    def refactor(self, s: str) -> str:
        # CharSplit has a bug that causes the splitter to behave unnatural if a - is present, so I fix this here
        s = str(s).replace("-", " ")

        compounds = self._split(s)
        print(s, compounds)
        # FIXME: filter out compounds that start with a non-alphanumerical character (e.g. brackets)
        abbreviation = "".join([compound[:1] for compound in compounds])

        return abbreviation
