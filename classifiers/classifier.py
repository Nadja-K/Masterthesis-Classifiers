from abc import ABCMeta, abstractmethod
from typing import Tuple, List, Set, Dict
import sqlite3
import datetime

from eval.evaluation import Evaluator


class Classifier(metaclass=ABCMeta):
    def __init__(self):
        self._loaded_datasplit = None
        self._data = None
        self._mention_entity_duplicate_count = {}
        self._entities = None

    def _load_datasplit(self, dataset_db_name: str, dataset_split: str, skip_trivial_samples: bool = False,
                        load_context: bool = False):
        assert dataset_split in ['train', 'test', 'val']

        curs, connection = self._connect_db(dataset_db_name)
        if skip_trivial_samples:
            print("Trivial samples will be skipped.")

        if load_context:
            print("Context sentences will be loaded. This can take a while.")

        self._data = self._retrieve_datasplit(curs, split=dataset_split, skip_trivial_samples=skip_trivial_samples,
                                              load_context=load_context)
        # self._mention_entity_duplicate_count = self._collect_mention_entity_duplicate_count(self._data)
        self._entities = set([x['entity_title'] for x in self._data])
        self._loaded_datasplit = dataset_split

        # Some statistical information
        print("Found %s sentences for %s entities for the %s split." % (len(self._data), len(self._entities),
                                                                        dataset_split))

        self._close_db(connection)

    def _retrieve_datasplit(self, curs: sqlite3.Cursor, split: str = 'train', skip_trivial_samples: bool = False,
                            load_context: bool = False) -> List[sqlite3.Row]:
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
            INNER JOIN splits 
              ON splits.id = entity_articles.id 
            WHERE splits.split = ? 
        """
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

        curs.execute(command, (split,))
        data = curs.fetchall()

        return data

    def _collect_mention_entity_duplicate_count(self, data: List[sqlite3.Row]) -> Dict[str, Dict[str, int]]:
        """
        Count how many samples with duplicate mentions exist per entity.
        This is necessary in order to average the evaluation metric later so that mentions that appear often in
        samples do not falsify the results.
        """
        mention_entity_duplicate_count = {}
        for sample in data:
            entity = sample['entity_title']
            mention = sample['mention']

            if entity not in mention_entity_duplicate_count:
                mention_entity_duplicate_count[entity] = {}

            if mention not in mention_entity_duplicate_count[entity]:
                mention_entity_duplicate_count[entity][mention] = 1
            else:
                mention_entity_duplicate_count[entity][mention] += 1

        return mention_entity_duplicate_count

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
    def evaluate_datasplit(self, split: str, eval_mode: str='mentions'):
        assert eval_mode in ['mentions', 'samples']
        start = datetime.datetime.now()

        eval_results = {}
        for sample in self._data:
            mention = sample['mention']
            entity = sample['entity_title']
            suggestions = self._classify(mention)

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
        eval = Evaluator()
        eval.evaluate(eval_results, eval_mode)
        # FIXME: nice print
        # macro, micro = eval.evaluate(eval_results, data)
        # print("\nMacro metrics:"
        #       "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % macro)
        # print("\nMicro metrics:"
        #       "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % micro)


