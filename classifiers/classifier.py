from abc import ABCMeta, abstractmethod
from typing import Tuple, List, Set, Dict, Union
import sqlite3
import datetime

from eval.evaluation import Evaluator


class Classifier(metaclass=ABCMeta):
    def __init__(self, dataset_db_name: str, dataset_split: str, split_table_name: str='splits',
                 skip_trivial_samples: bool = False, load_context: bool = False):
        self._loaded_datasplit = None
        self._query_data = None
        self._context_data = None
        self._mention_entity_duplicate_count = {}
        self._entities = None

        self._dataset_db_name = dataset_db_name

        # Load the specified datasplit
        assert dataset_split in ['train', 'test', 'val']
        self._load_datasplit(dataset_db_name, dataset_split, split_table_name=split_table_name,
                             skip_trivial_samples=skip_trivial_samples,
                             load_context=load_context)

    def _load_datasplit(self, dataset_db_name: str, dataset_split: str, split_table_name: str = 'splits',
                        skip_trivial_samples: bool = False, load_context: bool = False):
        assert dataset_split in ['train', 'test', 'val']

        curs, connection = self._connect_db(dataset_db_name)
        if skip_trivial_samples:
            print("Trivial samples will be skipped.")

        if load_context:
            print("Context sentences will be loaded. This can take a while.")

        self._query_data, self._context_data = self._retrieve_datasplit(curs, split=dataset_split,
                                                                        split_table_name=split_table_name,
                                                                        skip_trivial_samples=skip_trivial_samples,
                                                                        load_context=load_context)
        self._entities = set([x['entity_title'] for x in self._query_data])
        self._loaded_datasplit = dataset_split

        # Some statistical information
        print("Found %s query sentences, %s context sentences and %s entities for the %s split of "
              "the %s table." % (len(self._query_data), len(self._context_data), len(self._entities),
                                 dataset_split, split_table_name))
        self._close_db(connection)

    def _retrieve_datasplit(self, curs: sqlite3.Cursor, split: str = 'train', split_table_name: str='splits',
                            skip_trivial_samples: bool = False,
                            load_context: bool = False) -> Tuple[List[sqlite3.Row], List[sqlite3.Row]]:
        """
        Load a split from the dataset database.

        :param curs: cursor for the dataset DB.
        :param split: flag that indicates which split should be loaded ['train', 'test', 'val']
        :param load_context: flag that indicates whether the refactored context sentences of an backlink article
               are retrieved as well or not.

        :return: Contains all (sentence, mention, entity_title, backlink_title(, backlink_text)) tuples
        """
        command_head = """
            SELECT  sentences.mention, 
                    sentences.sentence, 
                    sentences.entity_id,
                    entity_articles.title as entity_title, 
                    backlink_articles.title as backlink_title
        """
        command_context = """
            , backlink_articles.text as backlink_text
        """
        command_body = """
            FROM sentences 
            INNER JOIN (articles) entity_articles 
              ON entity_articles.id = sentences.entity_id
            INNER JOIN (articles) backlink_articles 
              ON backlink_articles.id = sentences.backlink_id 
            INNER JOIN %s 
              ON %s.sample_id = sentences.rowid 
            WHERE %s.data_split = ?
            AND %s.query_context_split = ? 
            AND LENGTH(trim(sentences.mention)) > 0 
            AND instr(sentences.sentence, trim(sentences.mention)) > 0            
        """ % (split_table_name, split_table_name, split_table_name, split_table_name)
        command_skip_trivial_samples = """
            AND LOWER(REPLACE(sentences.mention, '_', ' ')) != LOWER(REPLACE(entity_title, '_', ' '))
        """

        # FIXME: shuffle data
        if load_context:
            command = command_head + command_context + command_body
        else:
            command = command_head + command_body
        if skip_trivial_samples:
            command = command + command_skip_trivial_samples

        curs.execute(command, (split, 'query'))
        query_data = curs.fetchall()
        curs.execute(command, (split, 'context'))
        context_data = curs.fetchall()

        return self._filter_out_empty_entities(query_data, context_data, skip_trivial_samples)

    def _filter_out_empty_entities(self, query_data: List[sqlite3.Row], context_data: List[sqlite3.Row],
                                   skip_trivial_samples: bool) -> Tuple[List[sqlite3.Row], List[sqlite3.Row]]:
        """
        If trivial samples are filtered out, it is possible that entities are left with either 0 query or context
        sentences. These entities can't be used for the context based classifiers, so they have to be filtered out
        manually here (since I couldn't come up with a sql query that takes care of this).
        """
        query_entities = set([x['entity_title'] for x in query_data])
        context_entities = set([x['entity_title'] for x in context_data])

        if not skip_trivial_samples:
            assert query_entities == context_entities, "The context and query samples do not share the same entities"
            return query_data, context_data

        trivial_entities = query_entities ^ context_entities

        filtered_query_data = [sample for sample in query_data if sample['entity_title'] not in trivial_entities]
        filtered_context_data = [sample for sample in context_data if sample['entity_title'] not in trivial_entities]

        filtered_query_entities = set([x['entity_title'] for x in filtered_query_data])
        filtered_context_entities = set([x['entity_title'] for x in filtered_context_data])
        assert filtered_query_entities == filtered_context_entities, "The filtered context and query samples do not " \
                                                                     "share the same entities"

        return filtered_query_data, filtered_context_data

    def _connect_db(self, db_name: str, timeout: float = 300.0) -> Tuple[sqlite3.Cursor, sqlite3.Connection]:
        connection = sqlite3.connect(db_name, timeout=timeout)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA synchronous = OFF")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("BEGIN TRANSACTION")
        curs = connection.cursor()

        return curs, connection

    def _close_db(self, connection: sqlite3.Connection):
        connection.commit()
        connection.close()

    @abstractmethod
    def _classify(self, mention: str, sentence: str, num_results: int=1) -> Dict[str, Union[float, int]]:
        """
        Internal classify method that collects raw results that might be interesting for statistics.
        """
        pass

    @abstractmethod
    def classify(self, mention: str, sentence: str) -> Set[Tuple[str, float]]:
        """
        Public classify method that users can use to classify a given string including some sort of similarity measure.
        """
        pass

    @abstractmethod
    def evaluate_datasplit(self, split: str, num_results: int = 1, eval_mode: str= 'mentions'):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        assert split in ['train', 'test', 'val']

        assert eval_mode in ['mentions', 'samples']
        start = datetime.datetime.now()

        eval_results = {}
        for sample in self._query_data:
            sentence = sample['sentence']
            mention = sample['mention']
            entity = sample['entity_title']
            # if eval_sentences:
            #     suggestions = self._classify(sentence, num_results)
            # else:
            #     suggestions = self._classify(mention, num_results)
            suggestions = self._classify(mention, sentence=sentence, num_results=num_results)

            if 'sentence' not in suggestions:
                suggestions['sentence'] = sample['sentence']

            if entity not in eval_results:
                eval_results[entity] = {}

            if mention not in eval_results[entity]:
                eval_results[entity][mention] = []

            eval_results[entity][mention].append(suggestions)

        end = datetime.datetime.now()
        print("Classification took: ", end - start)

        # Calculate some metrics
        evaluator = Evaluator()
        top1_accuracy, macro, micro = evaluator.evaluate(eval_results, eval_mode)

        print("\nTop1 Accuracy: %.2f%%" % top1_accuracy)
        print("\nMacro metrics:"
              "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % macro)
        print("\nMicro metrics:"
              "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % micro)


