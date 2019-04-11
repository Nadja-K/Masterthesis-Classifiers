import string

from classifier import Classifier
from Levenshtein import ratio  # https://github.com/ztane/python-Levenshtein
from nltk import SnowballStemmer
from nltk.corpus import stopwords
import re

from typing import Tuple


class RuleClassifier(Classifier):
    def __init__(self, dataset_db_name: str):
        super().__init__(dataset_db_name)
        self.stemmer = SnowballStemmer('german')
        self.stop_words = stopwords.words('german')
        # self.punctuation_regex = re.compile("(\W|_)", flags=re.U | re.I)

    def classify_datasplit(self, split, threshold=0.5):
        assert split in ['train', 'test', 'val']

        if split == 'train':
            data = self.train_data
        elif split == 'test':
            data = self.test_data
        else:
            data = self.val_data

        true_positive_count = 0
        for sample in data:
            mention = str(sample['mention'])
            reference_entity = str(sample['entity_title'])
            ratio, s1, s2 = self.classify(mention, reference_entity)
            # print(ratio, s1, s2)
            if ratio >= threshold:
                true_positive_count += 1
            else:
                print("{0: <30} {1: <30} {2: <30}".format(ratio, s1, s2))

        print("\nTP: %s" % (true_positive_count))
        print("Total: %s" % (len(data)))
        print("%.2f%% entities were classified correctly." % (100/len(data)*true_positive_count))

    def _remove_stopwords(self, s: str) -> str:
        words = s.split(" ")
        return ' '.join([word for word in words if word not in self.stop_words])

    def _heuristic_punctuation(self, s1: str, s2: str) -> Tuple[str, str]:
        def remove_punctuation(s):
            # return self.punctuation_regex.sub(" ", s)
            return s.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).replace(' '*4, ' ')\
                .replace(' '*3, ' ').replace(' '*2, ' ').strip()

        return remove_punctuation(s1), remove_punctuation(s2)

    def _heuristic_stemming(self, s1: str, s2: str) -> Tuple[str, str]:
        def stem_string_sequence(s):
            words = []
            s_words = s.split(" ")
            for word in s_words:
                words.append(self.stemmer.stem(word))
            return " ".join(words)

        return stem_string_sequence(s1), stem_string_sequence(s2)

    def _heuristic_lemmatization(self, s1: str, s2: str) -> Tuple[str, str]:
        pass

    def _heuristic_abbreviations(self, s1: str, s2: str) -> Tuple[str, str]:
        if len(s1) > len(s2):
            # Case: s2 might be the abbreviation
            return ''.join([s[0] for s in s1.split(" ")]), s2
        else:
            # Case: s1 might be the abbreviation
            return s1, ''.join([s[0] for s in s2.split(" ")])

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

    def classify(self, mention: str, reference_entity: str):
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
        # FIXME: we do not have any negative samples --> nachfragen?

        # Initialize the highest_sim value
        highest_sim = (ratio(mention, reference_entity), mention, reference_entity)

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

        # Heuristic: word Splitter u. 1 Buchstaben jeweils behalten
        tmp1, tmp2 = self._heuristic_abbreviations(highest_sim[1], highest_sim[2])
        highest_sim_tmp = self._check_similarity(tmp1, tmp2, highest_sim)
        # highest_sim = (highest_sim_tmp[0], highest_sim[1] + " | " + highest_sim_tmp[1], highest_sim[2] + " | " + highest_sim_tmp[2])
        highest_sim = (highest_sim_tmp[0], highest_sim[1], highest_sim[2])

        # FIXME: Heuristic: Compound Splitter u. 1 Buchstaben jeweils behalten
        # Note: incorporate into the above heuristic somehow?
        # Note2: definitely don't use the returned string from the above heuristic as input for this one

        # Return a 'similarity' value (percentage) of the two strings/entities based on real minimal edit distance
        return highest_sim
