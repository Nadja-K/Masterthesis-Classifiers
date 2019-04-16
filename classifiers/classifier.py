from abc import ABCMeta, abstractmethod
from typing import Tuple, List, Set, Dict
import sqlite3


class Classifier(metaclass=ABCMeta):
    def __init__(self):
        self.train_data = None
        self.test_data = None
        self.val_data = None
        self.train_entities = None
        self.test_entities = None
        self.val_entities = None

    def load_datasets(self, dataset_db_name: str, skip_trivial_samples: bool = False, load_context: bool = False):
        curs, connection = self._connect_db(dataset_db_name)

        if skip_trivial_samples:
            print("Trivial samples will be skipped.")

        if load_context:
            print("Context sentences will be loaded. This can take a while.")

        # Retrieve all samples from the database (corresponding to their split)
        self.train_data = self._load_split(curs, split='train', skip_trivial_samples=skip_trivial_samples,
                                           load_context=load_context)
        self.test_data = self._load_split(curs, split='test', skip_trivial_samples=skip_trivial_samples,
                                          load_context=load_context)
        self.val_data = self._load_split(curs, split='val', skip_trivial_samples=skip_trivial_samples,
                                         load_context=load_context)

        # Collect a set of all entities per dataset
        self.train_entities = set([x['entity_title'] for x in self.train_data])
        self.test_entities = set([x['entity_title'] for x in self.test_data])
        self.val_entities = set([x['entity_title'] for x in self.val_data])

        # Some statistical information
        print("Found %s sentences for %s entities for the training split." % (len(self.train_data), len(self.train_entities)))
        print("Found %s sentences for %s entities for the test split." % (len(self.test_data), len(self.test_entities)))
        print("Found %s sentences for %s entities for the val split." % (len(self.val_data), len(self.val_entities)))

        self._close_db(connection)

    def _load_split(self, curs: sqlite3.Cursor, split: str = 'train',
                    skip_trivial_samples: bool = False, load_context: bool = False) -> List[sqlite3.Row]:
        """
        Load a split from the dataset database.

        :param curs: cursor for the dataset DB.
        :param split: flag that indicates which split should be loaded ['train', 'test', 'val']
        :param load_context: flag that indicates whether the refactored context sentences of an backlink article
               are retrieved as well or not.

        :return: Contains all (sentence, mention, entity_title, backlink_title(, backlink_text)) tuples
        """
        # FIXME: remove the positive part from the databases and then remove it here as well +  remove it from the code project
        command_head = """
            SELECT  sentences.mention, 
                    sentences.sentence, 
                    entity_articles.title as entity_title, 
                    backlink_articles.title as backlink_title, 
                    sentences.positive as positive
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
            AND sentences.positive = 1
        """
        command_skip_trivial_samples = """
            AND sentences.mention != entity_title
        """

        # FIXME: shuffle data
        if load_context:
            command = command_head + command_context + command_body
        else:
            command = command_head + command_body
        if skip_trivial_samples:
            command = command + command_skip_trivial_samples

        curs.execute(command, (split,))
        return curs.fetchall()

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
    def evaluate_datasplit(self, split: str):
        pass


