from typing import NamedTuple, Tuple, Dict, Union, List, Set

import sys

epsilon = sys.float_info.epsilon

ComparisonResult = NamedTuple('ComparisonResult', [('tp', int), ('fp', int), ('tn', int), ('fn', int)])
ValidationResult = NamedTuple('ValidationResult', [('precision', float), ('recall', float), ('f_measure', float)])


def precision(tp: int, fp: int) -> float:
    if (tp + fp) == 0:
        return 0
    else:
        return tp / (tp + fp)


def recall(tp: int, fn: int) -> float:
    if (tp + fn) == 0:
        return 0
    else:
        return tp / (tp + fn)


def f_measure(precision, recall) -> float:
    if (precision + recall) == 0:
        return 0
    else:
        return 2 * ((precision * recall) / (precision + recall))


class Evaluator:
    def __init__(self):
        self._count_mentions = 0

        self._macro_precision = 0.0
        self._macro_recall = 0.0
        self._macro_f1_score = 0.0

        self._micro_precision = 0.0
        self._micro_recall = 0.0
        self._micro_f1_score = 0.0

        self._top1_accuracy = 0.0

        self._tp = 0
        self._fp = 0
        self._fn = 0

    def _precision(self) -> float:
        return self._macro_precision / self._count_mentions

    def _recall(self) -> float:
        return self._macro_recall / self._count_mentions

    def _accuracy(self) -> float:
        return self._top1_accuracy / self._count_mentions

    def evaluate(self, eval_results: Dict[str, Dict[str, List[Dict[str, Union[str, float, List[str]]]]]]
                 ) -> Tuple[float, ValidationResult, ValidationResult]:
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
                    if gt_entity in sample['suggestions']:
                        tp = 1
                        fp = len(sample['suggestions']) - 1
                    else:
                        fn = 1
                        fp = len(sample['suggestions'])

                    mention_precision += precision(tp, fp)
                    mention_recall += recall(tp, fn)

                    mention_tp += tp
                    mention_fn += fn
                    mention_fp += fp

                num_samples = len(samples)
                self._top1_accuracy += accuracy_tp / num_samples
                self._macro_precision += mention_precision / num_samples
                self._macro_recall += mention_recall / num_samples
                self._tp += mention_tp / num_samples
                self._fn += mention_fn / num_samples
                self._fp += mention_fp / num_samples
                self._count_mentions += 1

        self._top1_accuracy = self._accuracy()
        self._macro_precision = self._precision() * 100.
        self._macro_recall = self._recall() * 100.
        self._macro_f1_score = f_measure(self._macro_precision, self._macro_recall)

        self._micro_precision = precision(self._tp, self._fp) * 100.
        self._micro_recall = recall(self._tp, self._fn) * 100.
        self._micro_f1_score = f_measure(self._micro_precision, self._micro_recall)

        # FIXME: remove this again later
        print("%s\n%s\n%s" % (self._tp, self._fp, self._fn))
        print(self._top1_accuracy)
        print("%s\n%s\n%s" % (self._macro_precision, self._macro_recall, self._macro_f1_score))
        print("%s\n%s\n%s" % (self._micro_precision, self._micro_recall, self._micro_f1_score))

        return self._top1_accuracy, ValidationResult(
            self._macro_precision, self._macro_recall, self._macro_f1_score), ValidationResult(
            self._micro_precision, self._micro_recall, self._micro_f1_score)
#
#
# class RuleEvaluator(Evaluator):
#     def __init__(self):
#         super().__init__()
#         self._tp = 0
#         self._fp = 0
#         self._fn = 0
#
#     def evaluate(self, eval_results: Dict[str, Dict[str, Union[str, List[SuggestItem], int, Heuristic]]],
#                  data: Dict[str, Set[str]], print_samples: bool = True) -> Tuple[ValidationResult, ValidationResult]:
#         """
#         Calculate macro metrics for the given eval results and their ground truth data.
#         """
#         if print_samples:
#             print("{:40}{:40}{:40}{:40}".format("Mention", "TP entities", "FP entities", "FN entities"))
#             print("{:40}{:40}{:40}{:40}".format("-" * 15, "-" * 15, "-" * 15, "-" * 15))
#
#         for mention, res in eval_results.items():
#             matched_entities = set()
#             for suggestion in res['suggestions']:
#                 matched_entities.update(suggestion.reference_entities)
#
#             tp_entities = data[mention] & matched_entities
#             fn_entities = data[mention] - matched_entities
#             fp_entities = matched_entities - data[mention]
#
#             if print_samples:
#                 print("{:40}{:40}{:40}{:40}".format(mention, str(tp_entities), str(fp_entities), str(fn_entities)))
#
#             # Macro metric
#             self._macro_precision += precision(len(tp_entities), len(fp_entities))
#             self._macro_recall += recall(len(tp_entities), len(fn_entities))
#
#             # Micro metric
#             self._tp += len(tp_entities)
#             self._fp += len(fp_entities)
#             self._fn += len(fn_entities)
#
#         self._count_evaluate = len(eval_results)
#         macro_precision = self._precision() * 100
#         macro_recall = self._recall() * 100
#         macro_f1_score = f_measure(macro_precision, macro_recall)
#
#         micro_precision = precision(self._tp, self._fp) * 100
#         micro_recall = recall(self._tp, self._fn) * 100
#         micro_f1_score = f_measure(micro_precision, micro_recall)
#
#         # # FIXME: remove this again later
#         # print("%s\n%s\n%s" % (self._tp, self._fp, self._fn))
#         # print("%s\n%s\n%s" % (macro_precision, macro_recall, macro_f1_score))
#         # print("%s\n%s\n%s" % (micro_precision, micro_recall, micro_f1_score))
#
#         return ValidationResult(macro_precision, macro_recall, macro_f1_score), ValidationResult(
#             micro_precision, micro_recall, micro_f1_score)
