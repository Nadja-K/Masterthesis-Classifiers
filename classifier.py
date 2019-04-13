from abc import ABCMeta, abstractmethod
from typing import Tuple, List
import sqlite3


class Classifier(metaclass=ABCMeta):
    def __init__(self, dataset_db_name: str, load_negative_samples: bool = False, skip_trivial_samples: bool = False,
                 load_context: bool = False):
        self._load_dataset(dataset_db_name, load_negative_samples, skip_trivial_samples, load_context)

    def _load_dataset(self, dataset_db_name: str, load_negative_samples: bool = False,
                      skip_trivial_samples: bool = False, load_context: bool = False):
        curs, connection = self._connect_db(dataset_db_name)

        if load_negative_samples:
            print("Negative samples will be loaded.")
        else:
            print("Only positive samples will be loaded.")

        if skip_trivial_samples:
            print("Trivial samples will be skipped.")

        if load_context:
            print("Context sentences will be loaded. This can take a while.")

        self.train_data = self._load_split(curs, split='train', load_negative_samples=load_negative_samples,
                                           skip_trivial_samples=skip_trivial_samples, load_context=load_context)
        self.test_data = self._load_split(curs, split='test', load_negative_samples=load_negative_samples,
                                          skip_trivial_samples=skip_trivial_samples, load_context=load_context)
        self.val_data = self._load_split(curs, split='val', load_negative_samples=load_negative_samples,
                                         skip_trivial_samples=skip_trivial_samples, load_context=load_context)

        # Some statistical information about the splits
        train_entities = set([x['entity_title'] for x in self.train_data])
        test_entities = set([x['entity_title'] for x in self.test_data])
        val_entities = set([x['entity_title'] for x in self.val_data])

        print("Found %s sentences for %s entities for the training split." % (len(self.train_data), len(train_entities)))
        print("Found %s sentences for %s entities for the test split." % (len(self.test_data), len(test_entities)))
        print("Found %s sentences for %s entities for the val split." % (len(self.val_data), len(val_entities)))

        self._close_db(connection)

    def _load_split(self, curs: sqlite3.Cursor, split: str = 'train', load_negative_samples: bool = False,
                    skip_trivial_samples: bool = False, load_context: bool = False) -> List[sqlite3.Row]:
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
        """
        command_positive_samples_only = """
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
        if not load_negative_samples:
            command = command + command_positive_samples_only
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
    def classify(self):
        pass
