from typing import NamedTuple, Tuple, Dict, Union, List, Set

import logging
import sys

log = logging.getLogger('sampleOutput')
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
        self._count_valid_samples = 0

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

    def _clear_scores(self):
        self.__init__()

    def _precision(self) -> float:
        return self._macro_precision / self._count_valid_samples

    def _recall(self) -> float:
        return self._macro_recall / self._count_valid_samples

    def _accuracy(self) -> float:
        return self._top1_accuracy / self._count_valid_samples

    def _evaluate_sample(self, gt_entity: str, sample: Dict[str, Union[float, Set[str], str]], mention: str
                         ) -> Tuple[int, int, int, int]:
        suggestions = [str(x) for x in sample['suggestions']]
        len_suggestions = len(suggestions)
        tp, fp, fn = (0, 0, 0)
        accuracy_tp = 0

        # For the accuracy, we only take a look at the first suggestion
        if len_suggestions > 0 and sorted(suggestions)[0] == gt_entity:
            accuracy_tp += 1

        # Check the number of TP, FP and FN in the suggestions
        if gt_entity in suggestions:
            tp = 1
            fp = len_suggestions - 1

            # fp_entities = set(suggestions) - set([gt_entity])
            d = {'label': 'TP', 'mention': mention, 'tp_fn_entity': gt_entity, 'sentence': sample['sentence']}
            log.info('', extra=d)
        else:
            fn = 1
            fp = len_suggestions

            d = {'label': 'FN', 'mention': mention, 'tp_fn_entity': gt_entity, 'sentence': sample['sentence']}
            log.info('', extra=d)

        return tp, fp, fn, accuracy_tp

    def _evaluate_mentions(self, eval_results: Dict[str, Dict[str, List[Dict[str, Union[str, float, List[str]]]]]]
                           ) -> Tuple[float, ValidationResult, ValidationResult]:
        """
        Samples with duplicate mentions have the same impact on the final score as samples with rare mentions.
        Example:    Given 11 Samples where 10 Samples have the mention 'Astro-Physik' and one has the mention
                    'astrophysikalisch'. In this method, an average score per MENTION will be calculated, so that each
                    MENTION contributes equally to the final score regardless of the number of samples per mention.
        """
        for gt_entity, mentions in eval_results.items():
            gt_entity = str(gt_entity)
            for mention, samples in mentions.items():
                accuracy_tp, mention_precision, mention_recall = (0, 0, 0)
                mention_tp, mention_fp, mention_fn = (0, 0, 0)

                for sample in samples:
                    tp, fp, fn, accuracy_tmp = self._evaluate_sample(gt_entity, sample, mention)

                    accuracy_tp += accuracy_tmp
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
                self._count_valid_samples += 1

        self._top1_accuracy = self._accuracy() * 100.
        self._macro_precision = self._precision() * 100.
        self._macro_recall = self._recall() * 100.
        self._macro_f1_score = f_measure(self._macro_precision, self._macro_recall)

        self._micro_precision = precision(self._tp, self._fp) * 100.
        self._micro_recall = recall(self._tp, self._fn) * 100.
        self._micro_f1_score = f_measure(self._micro_precision, self._micro_recall)

        return self._top1_accuracy, ValidationResult(
            self._macro_precision, self._macro_recall, self._macro_f1_score), ValidationResult(
            self._micro_precision, self._micro_recall, self._micro_f1_score)

    def _evaluate_samples(self, eval_results: Dict[str, Dict[str, List[Dict[str, Union[str, float, List[str]]]]]]
                          ) -> Tuple[float, ValidationResult, ValidationResult]:
        """
        Samples with duplicate mentions have a larger impact on the final score as samples with rare mentions.
        Example:    Given 11 Samples where 10 Samples have the mention 'Astro-Physik' and one has the mention
                    'astrophysikalisch'. In this method all 11 SAMPLES would contribute equally to the final score
                    even though 9 of the 10 Astro-Physik samples will be trivial for the rule-based classifier,
                    which will result in a rather high final score.
        """
        for gt_entity, mentions in eval_results.items():
            gt_entity = str(gt_entity)
            for mention, samples in mentions.items():
                for sample in samples:
                    tp, fp, fn, accuracy_tmp = self._evaluate_sample(gt_entity, sample, mention)

                    self._top1_accuracy += accuracy_tmp
                    self._macro_precision += precision(tp, fp)
                    self._macro_recall += recall(tp, fn)
                    self._tp += tp
                    self._fp += fp
                    self._fn += fn
                    self._count_valid_samples += 1

        self._top1_accuracy = self._accuracy() * 100.
        self._macro_precision = self._precision() * 100.
        self._macro_recall = self._recall() * 100.
        self._macro_f1_score = f_measure(self._macro_precision, self._macro_recall)

        self._micro_precision = precision(self._tp, self._fp) * 100.
        self._micro_recall = recall(self._tp, self._fn) * 100.
        self._micro_f1_score = f_measure(self._micro_precision, self._micro_recall)

        return self._top1_accuracy, ValidationResult(
            self._macro_precision, self._macro_recall, self._macro_f1_score), ValidationResult(
            self._micro_precision, self._micro_recall, self._micro_f1_score)

    def evaluate(self, eval_results: Dict[str, Dict[str, List[Dict[str, Union[str, float, List[str]]]]]],
                 eval_mode: str='mentions') -> Tuple[float, ValidationResult, ValidationResult]:
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
        self._clear_scores()

        if eval_mode == 'mentions':
            scores = self._evaluate_mentions(eval_results)
        elif eval_mode == 'samples':
            scores = self._evaluate_samples(eval_results)

        # FIXME: remove this again later
        print("%s\n%s\n%s" % (self._tp, self._fp, self._fn))
        print(self._top1_accuracy)
        print("%s\n%s\n%s" % (self._macro_precision, self._macro_recall, self._macro_f1_score))
        print("%s\n%s\n%s" % (self._micro_precision, self._micro_recall, self._micro_f1_score))

        return scores
