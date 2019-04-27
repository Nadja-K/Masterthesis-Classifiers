from typing import NamedTuple, Tuple, Dict, Union, List, Set

import logging
import sys

log = logging.getLogger(__name__)
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


def f_measure(p: float, r: float) -> float:
    if (p + r) == 0:
        return 0
    else:
        return 2 * ((p * r) / (p + r))


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

        log.info('{:30}|{:30}|{:30}|{:30}|{:30}|{:5}'.format("GT_Entity", "Mention", "TP Entities", "FP Entities",
                                                             "FN Entities", "Distance"))
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

                        fp_entities = set(sample['suggestions']) - set([gt_entity])
                        log.info('{:30}|{:30}|{:30}|{:30}|{:30}|{:5}'.format(gt_entity, mention, gt_entity,
                                                                             ', '.join(fp_entities),
                                                                             '', sample['distance']))

                        # log.info("#TP: {:3}| #FN: {:3}| #FP: {:3}| Entity: {:30}| Mention: {:30}| Suggestions: {:40}| "
                        #          "Distance: {:5}".format(tp, 0, fp, gt_entity, mention,
                        #                                  ', '.join(sample['suggestions']), sample['distance']))
                    else:
                        fn = 1
                        fp = len(sample['suggestions'])

                        log.info('{:30}|{:30}|{:30}|{:30}|{:30}|{:5}'.format(gt_entity, mention, '',
                                                                             ', '.join(sample['suggestions']),
                                                                             gt_entity, sample['distance']))
                        # log.info("#TP: {:3}| #FN: {:3}| #FP: {:3}| Entity: {:30}| Mention: {:30}| Suggestions: {:40}| "
                        #          "Distance: {:5}".format(0, fn, fp, gt_entity, mention,
                        #                                  ', '.join(sample['suggestions']), sample['distance']))

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
