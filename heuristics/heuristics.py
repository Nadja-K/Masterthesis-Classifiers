from abc import ABCMeta, abstractmethod

from nltk import SnowballStemmer
from nltk.corpus import stopwords
from typing import List, Set, Tuple

from symspellpy.symspellpy import SymSpell, Verbosity, SuggestItem
from CharSplit import char_split

import string
import re


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

        self._sym_speller = None
        self._rule_mapping = {}

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def _refactor(self, s: str) -> str:
        pass

    def initialize_sym_speller(self):
        self._sym_speller = SymSpell(self.max_edit_distance_dictionary, self.prefix_length, self.count_threshold,
                                     self.compact_level)
        self._rule_mapping = {}

    def lookup(self, mention: str, original_mention: str = "") -> Tuple[List[SuggestItem], str]:
        """
        The original mention is optional here because it is only necessary for very specific heuristics.
        In the general case, it will be ignored and a previously refactored mention will be further refactored here.
        """
        refactored_mention = self._refactor(mention)
        suggestions = self._sym_speller.lookup(refactored_mention, Verbosity.CLOSEST)

        # Look up the unrefactored entities for the suggestions and save them
        for suggestion in suggestions:
            suggestion.reference_entities = self._rule_mapping[suggestion.term]

        return suggestions, refactored_mention

    def add_dictionary_entity(self, entity: str, original_entity: str = "") -> str:
        """
        Adds an entity to the sym spell dictionary of this heuristic.
        The original entity is usually not necessary except for very specific heuristics that rely on the original,
        untouched entity. Otherwise, the previously refactored entitiy is used here.
        """
        # Apply the current heuristic
        refactored_entity = self._refactor(entity)

        # Save the refactored entity in the heuristic symspeller + the mapping to the untouched entity
        self._sym_speller.create_dictionary_entry(refactored_entity, 1)
        if refactored_entity not in self._rule_mapping:
            self._rule_mapping[refactored_entity] = {original_entity}
        else:
            self._rule_mapping[refactored_entity].update({original_entity})

        return refactored_entity


class HeuristicOriginal(Heuristic):
    def name(self):
        return "original"

    def _refactor(self, s: str) -> str:
        return s


class HeuristicBrackets(Heuristic):
    """
    Remove brackets and their content from a string.
    Example: Höxter_(Schiff) -> Höxter_
    """
    def __init__(self):
        super().__init__()
        self._regex = re.compile("\(.*\)")

    def name(self):
        return "brackets"

    def _refactor(self, s: str) -> str:
        s = str(s)
        return self._regex.sub("", s)


class HeuristicPunctuation(Heuristic):
    def name(self):
        return "punctuation"

    def _refactor(self, s: str) -> str:
        s = str(s)
        return s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))\
            .replace(' ' * 4, ' ').replace(' ' * 3, ' ').replace(' ' * 2, ' ').strip()


class HeuristicLowercasing(Heuristic):
    def name(self):
        return "lowercasing"

    def _refactor(self, s: str) -> str:
        return s.lower()


class HeuristicStemming(Heuristic):
    """
    Note:   This heuristic does also lowercasing, however it primarily stems words.
            It is possible that a match would be found for the lowercased unstemmed version, so there is a separate
            lowercasing heuristic.
    """
    def __init__(self):
        super().__init__()
        self.stemmer = SnowballStemmer('german')

    def name(self):
        return "stemming"

    def _refactor(self, s: str) -> str:
        s = str(s)
        return " ".join([self.stemmer.stem(word) for word in s.split(" ")])


class HeuristicStopwords(Heuristic):
    def __init__(self):
        super().__init__()
        self.stop_words = stopwords.words('german')

    def name(self):
        return "stopwords"

    def _refactor(self, s: str) -> str:
        s = str(s)
        return ' '.join([word for word in s.split(" ") if word not in self.stop_words])


class HeuristicSort(Heuristic):
    def name(self):
        return "sort"

    def _refactor(self, s: str) -> str:
        s = str(s)
        return " ".join(sorted(s.split(" ")))


class HeuristicAbbreviationsCompounds(HeuristicPunctuation):
    """
    The abbreviation heuristic is far more complex than the other heuristics.
    This is because I can not know if the given query mention is already an abbreviation or the reference entity.
    Example:    Given the mention "embedded subscriber identity module" and the reference entity "eSIM".
                My system does not know if the mention is already an abbreviation or not.
                So instead I assume two possible cases:
                1) The mention is already an abbreviation
                2) The mention is not an abbreviation yet

                For the first case we have to assume that the reference entity is NOT an abbreviation (otherwise a
                prior heuristic should have found a match already).
                The same is valid for the second case, we have to assume that the reference entity IS an abbreviation.
                In order to check both cases I need the reference entities in two versions: original (without any
                stemming, only punctuation removal) and abbreviation.

                This heuristic checks both cases and returns the better result of the two.
    """
    def __init__(self, prob_threshold: float = 0.1, max_edit_distance_dictionary: int = 0):
        """
        :param prob_threshold: This threshold is used for the compound splitter. CharSplit returns a probability for
        how likely the compounds are for a word. All compounds that have a lower probability are discarded. Furthermore,
        this threshold is the condition to stop the recursive compound splitting.

        :param max_edit_distance_dictionary: A threshold to ensure that the matched abbreviation is as similar as
        possible to the reference entity.
        """
        super().__init__(max_edit_distance_dictionary=max_edit_distance_dictionary)
        assert prob_threshold > 0
        self._prop_threshold = prob_threshold
        # self._max_ldist = max_ldist
        self.max_edit_distance_dictionary = max_edit_distance_dictionary

        # The symspell dictionary and mapping for the unrefactored entities (case 1)
        self._original_sym_speller = None
        self._original_rule_mapping = None

    def name(self):
        return "abbreviations"

    def initialize_sym_speller(self):
        super().initialize_sym_speller()
        self._original_sym_speller = SymSpell(self.max_edit_distance_dictionary, self.prefix_length,
                                              self.count_threshold, self.compact_level)
        self._original_rule_mapping = {}

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
        abbreviation = "".join([compound if compound.isdigit() else compound[:1].capitalize() for compound in compounds])

        return abbreviation

    def lookup(self, mention: str, original_mention: str = "") -> Tuple[List[SuggestItem], str]:
        """
        The abbreviation heuristic only uses the original mention instead of a previously refactored mention.
        This is because previous refactoring might affect the compound splitting.
        """
        # Case1: the mention is the abbreviation, the original entity is not known as abbreviation
        # I only do a punctuation refactoring on the mention and then match against the abbreviation refactored entities
        case1_refactored_mention = super()._refactor(original_mention)
        case1_suggestions = self._sym_speller.lookup(case1_refactored_mention, Verbosity.CLOSEST)
        case1_distance = 99999
        for suggestion in case1_suggestions:
            suggestion.reference_entities = self._rule_mapping[suggestion.term]
            case1_distance = suggestion.distance

        # Case2: the mention is currently not an abbreviation but the original entity is only known as abbreviation
        # I do the abbreviation refactoring on the mention and then match against the punctuation refactored entities
        case2_refactored_mention = self._refactor(original_mention)
        case2_suggestions = self._original_sym_speller.lookup(case2_refactored_mention, Verbosity.CLOSEST)
        case2_distance = 99999
        for suggestion in case2_suggestions:
            suggestion.reference_entities = self._original_rule_mapping[suggestion.term]
            case2_distance = suggestion.distance

        # Only return the better result
        if case1_distance < case2_distance:
            return case1_suggestions, case1_refactored_mention
        else:
            return case2_suggestions, case2_refactored_mention

    def add_dictionary_entity(self, entity: str, original_entity: str = "") -> str:
        """
        This heuristic needs the refactored entity as well as the original entity in its dictionary because it is
        possible, that either the mention or the reference entity is the abbreviation.
        """
        # Add the entities in abbreviation form to the own sym spell dictionary
        original_entity = str(original_entity)
        abbreviation = self._refactor(original_entity)
        self._sym_speller.create_dictionary_entry(abbreviation, 1)
        if abbreviation not in self._rule_mapping:
            self._rule_mapping[abbreviation] = {original_entity}
        else:
            self._rule_mapping[abbreviation].update({original_entity})

        # Because the original entity could already be the abbreviation, we also want to save the original one.
        # Do the same for the mapping and apply the punctuation heuristic to the original entity.
        punctuation_refactored_entity = super()._refactor(original_entity)
        self._original_sym_speller.create_dictionary_entry(punctuation_refactored_entity, 1)
        if punctuation_refactored_entity not in self._original_rule_mapping:
            self._original_rule_mapping[punctuation_refactored_entity] = {original_entity}
        else:
            self._original_rule_mapping[punctuation_refactored_entity].update({original_entity})

        return abbreviation


class HeuristicAbbreviationsSpaces(HeuristicAbbreviationsCompounds):
    """
    Does the same as the parent heuristic HeuristicAbbreviationsCompounds except it does not split a string into
    compounds but rather only splits at spaces.
    """
    def _split(self, s: str) -> List[str]:
        split = s.split(" ")
        compounds = [split.strip().lower() for split in split]

        return compounds
