from classifiers.classifier import Classifier
from classifiers.rule_classifier import RuleClassifier
from classifiers.bert_classifier import BertEmbeddingClassifier
from utils.heuristics import *


class HybridClassifier(Classifier):
    def __init__(self, heuristics: List[Heuristic], dataset_db_name: str, dataset_split: str, annoy_metric: str,
                 bert_config_file: str, init_checkpoint: str, vocab_file: str, seq_len: int,
                 split_table_name: str='splits', skip_trivial_samples: bool = False, prefill_symspell: bool = True,
                 batch_size: int=32, layer_indexes: List[int]=[-1, -2, -3, -4], use_one_hot_embeddings: bool=False,
                 do_lower_case: bool=True, annoy_index_path: str=None, num_trees: int=30, annoy_output_dir: str='',
                 distance_allowance: float=0.05):

        # Load the data ONCE here
        super().__init__(dataset_db_name=dataset_db_name, dataset_split=dataset_split, split_table_name=split_table_name,
                         skip_trivial_samples=skip_trivial_samples, load_context=False)

        # Make an instance of the rule classifier and give the loaded data to it
        self.rule_classifier = RuleClassifier(heuristics=heuristics, dataset_db_name=dataset_db_name,
                                              dataset_split=dataset_split, split_table_name=split_table_name,
                                              skip_trivial_samples=skip_trivial_samples,
                                              prefill_symspell=prefill_symspell, query_data=self._query_data,
                                              context_data=self._context_data, entities=self._entities,
                                              loaded_datasplit=self._loaded_datasplit)

        # Do the same for the bert classifier
        self.bert_classifier = BertEmbeddingClassifier(dataset_db_name=dataset_db_name, dataset_split=dataset_split,
                                                       annoy_metric=annoy_metric, bert_config_file=bert_config_file,
                                                       init_checkpoint=init_checkpoint, vocab_file=vocab_file,
                                                       seq_len=seq_len, batch_size=batch_size,
                                                       layer_indexes=layer_indexes,
                                                       use_one_hot_embeddings=use_one_hot_embeddings,
                                                       do_lower_case=do_lower_case,
                                                       skip_trivial_samples=skip_trivial_samples,
                                                       split_table_name=split_table_name,
                                                       annoy_index_path=annoy_index_path, num_trees=num_trees,
                                                       annoy_output_dir=annoy_output_dir,
                                                       distance_allowance=distance_allowance,
                                                       query_data=self._query_data, context_data=self._context_data,
                                                       entities=self._entities, loaded_datasplit=self._loaded_datasplit)

        # Just some sanity checks
        import time
        eval_mode = "mentions"
        start = time.time()
        self.rule_classifier.evaluate_datasplit(dataset_split, eval_mode=eval_mode)
        print("Rule Evaluation took %s" % (time.time() - start))

        eval_mode = "samples"
        start = time.time()
        self.bert_classifier.evaluate_datasplit(dataset_split, eval_mode=eval_mode)
        print("Bert Evaluation took %s" % (time.time() - start))

        eval_mode = "mentions"
        start = time.time()
        self.rule_classifier.evaluate_datasplit(dataset_split, eval_mode=eval_mode)
        print("Rule Evaluation took %s" % (time.time() - start))

        eval_mode = "samples"
        start = time.time()
        self.bert_classifier.evaluate_datasplit(dataset_split, eval_mode=eval_mode)
        print("Bert Evaluation took %s" % (time.time() - start))

    # FIXME
    def _classify(self, mention: str, sentence: str, num_results: int=1):
        assert (self.rule_classifier._loaded_datasplit == self.bert_classifier._loaded_datasplit ==
                self._loaded_datasplit), "One of the classifiers has a different datasplit loaded"

        # Case 1: rule based finds exactly 1 entity
        # -> Return
        suggestions = self.rule_classifier._classify(mention, sentence)
        if len(suggestions['suggestions']) == 1:
            # print("Rule: ")
            # print(suggestions)
            pass
        # Case 2: rule based finds exactly 0 entities
        # -> Bert
        # Case 3: rule based finds > 1 entities
        # -> Bert
        else:
            suggestions = self.bert_classifier._classify(mention, sentence, num_results=1)
            # print("Bert: ")
            # print(suggestions)

        return suggestions

    # FIXME (is not correct yet)
    def classify(self, mention: str, sentence: str):
        assert (self.rule_classifier._loaded_datasplit == self.bert_classifier._loaded_datasplit ==
                self._loaded_datasplit), "One of the classifiers has a different datasplit loaded"

        res = self._classify(mention, sentence)
        return res['suggestions'][0]

    def evaluate_datasplit(self, dataset_split: str, num_results: int = 1, eval_mode: str= 'mentions'):
        assert num_results == 1, 'NUM_RESULTS should not be set for the rule-based classifier. Instead all results ' \
                                 'with the same distance are returned for this classifier.'

        self.rule_classifier._fill_symspell_dictionaries(dataset_split="val")
        assert (self._loaded_datasplit == 'val' and self.rule_classifier._loaded_datasplit == 'val' and
                self.bert_classifier._loaded_datasplit == 'val'), 'The evaluation could not be performed because one' \
                                                                  'of the classifiers had a different dataset loaded' \
                                                                  'than the "val" dataset. Only run the evaluation on' \
                                                                  'its own without manual classification requests.'

        super().evaluate_datasplit(dataset_split, num_results=num_results, eval_mode=eval_mode)
