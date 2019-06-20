import string
from typing import List
from CharSplit import char_split


punctuation_list = string.punctuation + '„“'


def remove_punctuation(s: str) -> str:
    s = str(s)
    refactored = s.replace('.', '')

    # For every other punctuation symbol (e.g. - or _) we want a space instead
    refactored = refactored.translate(str.maketrans(punctuation_list, ' ' * len(punctuation_list)))
    refactored = " ".join([word for word in refactored.split(" ") if len(word) > 0])
    # refactored = refactored.translate(str.maketrans(self._punctuation_list, ' ' * len(self._punctuation_list)))\
    #     .replace(' ' * 4, '').replace(' ' * 3, '').replace(' ' * 2, '').strip()

    return refactored


def split_compounds(s: str, prop_threshold: float=0.5) -> List[str]:
    """
    This method recursively splits an input string into its compounds based on a probability threshold.

    The compound splitter used in this function (CharSplit) only splits a string into two compounds.
    However, words can have far more relevant compounds. To solve this issue I recursively split the compounds
    into further compounds until they no longer satisfy the probability threshold.

    CharSplit has some other 'weaknesses' that are covered here.
    1) If the input string consists of multiple words separated by a space, CharSplit is unable to handle it very
       well. Usually the resulting probability is negative. Instead, I split the input string manually on spaces.
    2) CharSplit returns various splits (sorted by a probability) but to keep it simple, I only take the first one
       into consideration
    """
    s = remove_punctuation(s)

    if " " in s:
        split = s.split(" ")
        probability = 1.0
    else:
        split_res = char_split.split_compound(s)[0]
        probability = split_res[0]
        split = split_res[1:]
    compounds = [split.strip().lower() for split in split]
    # compounds = [split.strip() for split in split]

    if probability >= prop_threshold:
        recursive_compounds = []
        for compound in compounds:
            recursive_compounds.extend(split_compounds(compound, prop_threshold=prop_threshold))
        return recursive_compounds
    else:
        return [s]
