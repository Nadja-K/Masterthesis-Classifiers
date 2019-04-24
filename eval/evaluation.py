from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Tuple, Dict, Union, List, Set

import sys

from symspellpy.symspellpy import SuggestItem
from heuristics.heuristics import Heuristic

epsilon = sys.float_info.epsilon

ComparisonResult = NamedTuple('ComparisonResult', [('tp', int), ('fp', int), ('tn', int), ('fn', int)])
ValidationResult = NamedTuple('ValidationResult', [('precision', float), ('recall', float), ('f_measure', float)])

# FIXME: remove this later
"""
Code for fast testing:

from eval.evaluation import EmbeddingEvaluator
data = {
	'Arbeitsspeicher': 
	{
		'(Arbeits-)Speicher': {'suggestion': 'Arbeitsspeicher'}, 
		'Hauptspeicher': {'suggestion': 'Arbeitsspeicher'}, 
		'Speicher': {'suggestion': 'Speicher'}
	}, 
	'Amphore': 
	{
		'Amphoren': {'suggestion': 'Amphore'}, 
		'Transportgefäße': {'suggestion': ''}
	},
	'Buch':
	{
		'Buchformaten': {'suggestion': 'Buch'}
	}
}
eval = EmbeddingEvaluator()
x = eval.evaluate(data)
"""


def precision(tp: int, fp: int) -> float:
    return tp / (tp + fp + epsilon)


def recall(tp: int, fn: int) -> float:
    return tp / (tp + fn + epsilon)


def f_measure(precision, recall) -> float:
    return 2 * ((precision * recall) / (precision + recall + epsilon))


class Evaluator(metaclass=ABCMeta):
    def __init__(self):
        self._macro_precision = 0
        self._macro_recall = 0
        self._count_evaluate = 0

    def _precision(self) -> float:
        return self._macro_precision / self._count_evaluate

    def _recall(self) -> float:
        return self._macro_recall / self._count_evaluate


class EmbeddingEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        self._accuracy = 0

    def evaluate(self, eval_results: Dict[str, Dict[str, Set[Dict[str, Union[str, float]]]]]) -> float:
        """
        # FIXME: should 'suggestions' be a List of strings or really only ONE string?
        eval_results should be of the following structure:
        {
            'gt_entity_title_1':
            {
                'mention_1':
                {
                    {
                        'sentence': str,
                        'suggestion': str,
                        'probability': float
                    },
                    ...
                },
                ...
            },
            ...
        }

        Each mention can be present in multiple sentences and for multiple entities.
        I group the classified samples (= sentences) by their respective ground truth entity and text mention
        (unlike the rule based classifier, the embedding based classifier has to match EXACTLY ONE entity).
        Because it is using the context of a sentence (unlike the rule based classifier), this classifier needs to be
        able to decide which entity the present mention is actually referring true.
        Example: GB could refer to a machine part or Großbritannien. The rule-based classifier is allowed to match both
        because it can't use the context. The embedding based one however should know if the mention in this particular
        sentence refers to a machine part or actually Großbritannien.
        """
        for gt_entity, mentions in eval_results.items():
            tp = 0
            for mention, sample in mentions.items():
                if sample['suggestion'] == gt_entity:
                    tp += 1

            self._accuracy += tp / len(mentions)
            self._count_evaluate += 1
        self._accuracy /= self._count_evaluate

        print(self._accuracy)
        return self._accuracy
            # avg_entity_mention_precision = 0
            # avg_entity_mention_recall = 0
            # num_entity_mention_samples = len(mentions)

            # for mention, sample in mentions.items():
                # tp, fp, fn = (0, 0, 0)
                # if sample['suggestion'] == gt_entity:
                #     tp = 1
                # elif len(sample['suggestion']) > 0:
                #     fn = 1
                #     fp = 1
                # else:
                #     fn = 1
                # avg_entity_mention_precision += precision(tp, fp)
                # avg_entity_mention_recall += recall(tp, fn)
                # print(gt_entity, mention, tp, fp, fn)

        #     avg_entity_mention_precision /= num_entity_mention_samples
        #     avg_entity_mention_recall /= num_entity_mention_samples
        #     print(gt_entity, avg_entity_mention_precision, avg_entity_mention_recall)
        #
        #     # Macro metric
        #     self._macro_precision += avg_entity_mention_precision
        #     self._macro_recall += avg_entity_mention_recall
        #     self._count_evaluate += 1
        #
        # macro_precision = self._precision() * 100
        # macro_recall = self._recall() * 100
        # macro_f1_score = f_measure(macro_precision, macro_recall)
        #
        # return ValidationResult(macro_precision, macro_recall, macro_f1_score)


class RuleEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        self._tp = 0
        self._fp = 0
        self._fn = 0

    def evaluate(self, eval_results: Dict[str, Dict[str, Union[str, List[SuggestItem], int, Heuristic]]],
                 data: Dict[str, Set[str]], print_samples: bool = True) -> Tuple[ValidationResult, ValidationResult]:
        """
        Calculate macro metrics for the given eval results and their ground truth data.
        """
        if print_samples:
            print("{:40}{:40}{:40}{:40}".format("Mention", "TP entities", "FP entities", "FN entities"))
            print("{:40}{:40}{:40}{:40}".format("-" * 15, "-" * 15, "-" * 15, "-" * 15))

        for mention, res in eval_results.items():
            matched_entities = set()
            for suggestion in res['suggestions']:
                matched_entities.update(suggestion.reference_entities)

            tp_entities = data[mention] & matched_entities
            fn_entities = data[mention] - matched_entities
            fp_entities = matched_entities - data[mention]

            if print_samples:
                # FIXME remove this if condition later, rn only for printing needed
                if len(tp_entities) == 0:
                    print("{:40}{:40}{:40}{:40}".format(mention, str(tp_entities), str(fp_entities), str(fn_entities)))
                # print("{:40}{:40}{:40}{:40}".format(mention, str(tp_entities), str(fp_entities), str(fn_entities)))

            # Macro metric
            self._macro_precision += precision(len(tp_entities), len(fp_entities))
            self._macro_recall += recall(len(tp_entities), len(fn_entities))

            # Micro metric
            self._tp += len(tp_entities)
            self._fp += len(fp_entities)
            self._fn += len(fn_entities)

        self._count_evaluate = len(eval_results)
        macro_precision = self._precision() * 100
        macro_recall = self._recall() * 100
        macro_f1_score = f_measure(macro_precision, macro_recall)

        micro_precision = precision(self._tp, self._fp) * 100
        micro_recall = recall(self._tp, self._fn) * 100
        micro_f1_score = f_measure(micro_precision, micro_recall)

        # FIXME: remove this again later
        print("%s\n%s\n%s" % (self._tp, self._fp, self._fn))
        print("%s\n%s\n%s" % (macro_precision, macro_recall, macro_f1_score))
        print("%s\n%s\n%s" % (micro_precision, micro_recall, micro_f1_score))

        return ValidationResult(macro_precision, macro_recall, macro_f1_score), ValidationResult(
            micro_precision, micro_recall, micro_f1_score)
