from abc import ABCMeta, abstractmethod

from nltk import SnowballStemmer
from nltk.corpus import stopwords
from typing import List, Set

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
    def _refactor(self, s: str) -> str:
        pass

    def initialize_sym_speller(self):
        self.sym_speller = SymSpell(self.max_edit_distance_dictionary, self.prefix_length, self.count_threshold,
                                    self.compact_level)
        self.rule_mapping = {}

    def apply_heuristic(self, original_mention: str, previous_refactored_mention: str) -> str:
        """
        General method to apply a heuristic.
        Depending on the heuristic the previously refactored mention is used or the original (unrefactored) mention.
        """
        # For the abbreviation heuristic, use the original mention
        # The heuristic includes the punctuation heuristic
        if self.name() == 'abbreviations':
            refactored_mention = self._refactor(original_mention)
        else:
            refactored_mention = self._refactor(previous_refactored_mention)

        return refactored_mention

    def lookup_match(self, original_mention: str, refactored_mention: str) -> Set[str]:
        pass

    def add_dictionary_entity(self, entity: str, previous_refactored_entity: str) -> str:
        # Apply the current heuristic
        refactored_entity = self.apply_heuristic(entity, previous_refactored_entity)

        # Save the refactored entity in the heuristic symspeller + the mapping to the untouched entity
        self.sym_speller.create_dictionary_entry(refactored_entity, 1)
        if refactored_entity not in self.rule_mapping:
            self.rule_mapping[refactored_entity] = {entity}
        else:
            self.rule_mapping[refactored_entity].update({entity})

        return refactored_entity


class HeuristicPunctuation(Heuristic):
    def name(self):
        return "punctuation"

    def _refactor(self, s: str) -> str:
        s = str(s)
        return s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))\
            .replace(' ' * 4, ' ').replace(' ' * 3, ' ').replace(' ' * 2, ' ').strip()


class HeuristicStemming(Heuristic):
    def __init__(self):
        super().__init__()
        self.stemmer = SnowballStemmer('german')

    def name(self):
        return "stemming"

    def _refactor(self, s: str) -> str:
        return " ".join([self.stemmer.stem(word) for word in s.split(" ")])


class HeuristicStopwords(Heuristic):
    def __init__(self):
        super().__init__()
        self.stop_words = stopwords.words('german')

    def name(self):
        return "stopwords"

    def _refactor(self, s: str) -> str:
        return ' '.join([word for word in s.split(" ") if word not in self.stop_words])


class HeuristicSort(Heuristic):
    def name(self):
        return "sort"

    def _refactor(self, s: str) -> str:
        return " ".join(sorted(s.split(" ")))


class HeuristicAbbreviations(HeuristicPunctuation):
    def __init__(self, prob_threshold):
        super().__init__()
        assert prob_threshold > 0
        self._prop_threshold = prob_threshold
        # FIXME: explanation
        self.original_sym_speller = None
        self.original_rule_mapping = None

    def name(self):
        return "abbreviations"

    def initialize_sym_speller(self):
        super().initialize_sym_speller()
        self.original_sym_speller = SymSpell(self.max_edit_distance_dictionary, self.prefix_length,
                                             self.count_threshold, self.compact_level)
        self.original_rule_mapping = {}

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

    def _refactor(self, s: str) -> str:
        # CharSplit has a bug that causes the splitter to behave unnatural if a - is present, so I fix this here
        # by making sure no punctuation characters are in the string
        s = super()._refactor(s)
        compounds = self._split(s)

        # Create an abbreviation from the compounds. However, pure digit compounds are kept as is.
        abbreviation = "".join([compound if compound.isdigit() else compound[:1] for compound in compounds])
        # print(s, compounds, abbreviation)

        return abbreviation

    def add_dictionary_entity(self, entity: str, previous_refactored_entity: str) -> str:
        """
        This heuristic needs the refactored entity as well as the original entity in its dictionary because it is
        possible, that either the mention or the reference entity is the abbreviation.
        """
        entity = str(entity)
        refactored_entity = super().add_dictionary_entity(entity, previous_refactored_entity)

        # Because the original entity could already be the abbreviation, we also want to save this here.
        # Do the same for the mapping and apply the punctuation heuristic to the original entity.
        refactored_original_entity = super()._refactor(entity)
        self.original_sym_speller.create_dictionary_entry(refactored_original_entity, 1)
        if refactored_original_entity not in self.rule_mapping:
            self.original_rule_mapping[refactored_original_entity] = {entity}
        else:
            self.original_rule_mapping[refactored_original_entity].update({entity})

        return refactored_entity
