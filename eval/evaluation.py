from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Tuple, Dict, Union, List, Set

import sys
import sqlite3

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


# class Evaluator(metaclass=ABCMeta):
class Evaluator:
    def __init__(self):
        self._macro_precision = 0.0
        self._macro_recall = 0.0

        self._accuracy = 0.0

        self._tp = 0
        self._fp = 0
        self._fn = 0

    def _precision(self) -> float:
        return self._macro_precision / self._count_evaluate

    def _recall(self) -> float:
        return self._macro_recall / self._count_evaluate

    def evaluate(self, eval_results: List[Tuple[sqlite3.Row, Dict[str, Union[str, Set[str], int, Heuristic]]]]):
        """
        eval_results should be of the following structure:
        {
            'gt_entity_title_1':
            {
                'mention_1':
                [
                    {
                        'sentence': str,
                        'suggestions': List[str],
                        'distance': float
                    },
                    ...
                ],
                ...
            },
            ...
        }
        """
        # Accuracy only
        avg_accuracy = 0
        macro_precision, macro_recall = (0, 0)
        micro_tp, micro_fp, micro_fn = (0, 0, 0)
        count_mentions = 0
        for gt_entity, mentions in eval_results.items():
            for mention, samples in mentions.items():
                accuracy_tp, mention_precision, mention_recall = (0, 0, 0)
                mention_tp, mention_fp, mention_fn = (0, 0, 0)
                for sample in samples:
                    tp, fp, fn = (0, 0, 0)
                    # For the accuracy, we only take a look at the first suggestion
                    if len(sample['suggestions']) > 0 and sorted(sample['suggestions'])[0] == gt_entity:
                        accuracy_tp += 1

                    # Check the number of TP, FP and FN in the suggestions
                    # print(gt_entity, mention, sample['suggestions'], sample['heuristic'], sample['distance'], sample['refactored_mention'])
                    if gt_entity in sample['suggestions']:
                        tp = 1
                        fp = len(sample['suggestions']) - 1
                    else:
                        fn = 1
                        fp = len(sample['suggestions'])

                    if (tp + fp) != 0:
                        mention_precision += (tp / (tp + fp))

                    if (tp + fn) != 0:
                        mention_recall += (tp / (tp + fn))
                    mention_tp += tp
                    mention_fn += fn
                    mention_fp += fp

                print(mention, mention_precision, mention_recall, mention_tp, mention_fn, mention_fp)
                num_samples = len(samples)
                avg_accuracy += accuracy_tp / num_samples
                macro_precision += mention_precision / num_samples
                macro_recall += mention_recall / num_samples
                micro_tp += mention_tp / num_samples
                micro_fn += mention_fn / num_samples
                micro_fp += mention_fp / num_samples

                count_mentions += 1

        avg_accuracy /= count_mentions
        macro_precision /= count_mentions
        macro_recall /= count_mentions

        if (micro_tp + micro_fp) != 0:
            micro_precision = micro_tp / (micro_tp + micro_fp + epsilon)
        else:
            micro_precision = 0

        if (micro_tp + micro_fn) != 0:
            micro_recall = micro_tp / (micro_tp + micro_fn + epsilon)
        else:
            micro_recall = 0

        print(avg_accuracy, macro_precision, macro_recall, micro_precision, micro_recall)
        print(micro_tp, micro_fn, micro_fp)


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
                print("{:40}{:40}{:40}{:40}".format(mention, str(tp_entities), str(fp_entities), str(fn_entities)))

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

        # # FIXME: remove this again later
        # print("%s\n%s\n%s" % (self._tp, self._fp, self._fn))
        # print("%s\n%s\n%s" % (macro_precision, macro_recall, macro_f1_score))
        # print("%s\n%s\n%s" % (micro_precision, micro_recall, micro_f1_score))

        return ValidationResult(macro_precision, macro_recall, macro_f1_score), ValidationResult(
            micro_precision, micro_recall, micro_f1_score)
