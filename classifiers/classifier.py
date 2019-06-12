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
        self._query_data, self._context_data, self._entities, self._loaded_datasplit = Classifier.load_datasplit(
            dataset_db_name, dataset_split, split_table_name=split_table_name,
            skip_trivial_samples=skip_trivial_samples, load_context=load_context)

    @staticmethod
    def load_datasplit(dataset_db_name: str, dataset_split: str, split_table_name: str = 'splits',
                       skip_trivial_samples: bool = False, load_context: bool = False):
        assert dataset_split in ['train', 'test', 'val']

        curs, connection = Classifier._connect_db(dataset_db_name)
        if skip_trivial_samples:
            print("Trivial samples will be skipped.")

        if load_context:
            print("Context sentences will be loaded. This can take a while.")

        _query_data, _context_data = Classifier._retrieve_datasplit(curs, split=dataset_split,
                                                                    split_table_name=split_table_name,
                                                                    skip_trivial_samples=skip_trivial_samples,
                                                                    load_context=load_context)
        _entities = set([x['entity_title'] for x in _query_data])
        _loaded_datasplit = dataset_split

        # Some statistical information
        print("Found %s query sentences, %s context sentences and %s entities for the %s split of "
              "the %s table." % (len(_query_data), len(_context_data), len(_entities),
                                 dataset_split, split_table_name))
        Classifier._close_db(connection)

        return _query_data, _context_data, _entities, _loaded_datasplit

    @staticmethod
    def _retrieve_datasplit(curs: sqlite3.Cursor, split: str = 'train', split_table_name: str='splits',
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
            AND sentences.sentence NOT IN (
                SELECT tmp.sentence
                FROM sentences as tmp
                INNER JOIN %s
                    ON %s.sample_id = tmp.rowid
                WHERE (%s.data_split = ? or %s.data_split = ?)
            )
        """ % (split_table_name, split_table_name, split_table_name, split_table_name, split_table_name, split_table_name, split_table_name, split_table_name)
        command_skip_trivial_samples = """
            AND LOWER(REPLACE(sentences.mention, '_', ' ')) != LOWER(REPLACE(entity_title, '_', ' '))
        """
        disjoint_sentences_command = """
            AND sentence NOT IN (
                SELECT sentence
                FROM sentences
                INNER JOIN %s
                    ON %s.sample_id = sentences.rowid
                WHERE %s.data_split = ?
                AND %s.query_context_split = ?
                AND LENGTH(trim(sentences.mention)) > 0 
                AND instr(sentences.sentence, trim(sentences.mention)) > 0 
            )
        """ % (split_table_name, split_table_name, split_table_name, split_table_name)

        if load_context:
            command = command_head + command_context + command_body
        else:
            command = command_head + command_body
        if skip_trivial_samples:
            command = command + command_skip_trivial_samples

        # Make sure to remove all samples from the query split that have identical sentences in the context split
        other_splits = list(set(['train', 'test', 'val']) - {split})
        curs.execute(command + disjoint_sentences_command, (split, 'query', other_splits[0], other_splits[1], split, 'context'))
        query_data = curs.fetchall()
        curs.execute(command, (split, 'context', other_splits[0], other_splits[1]))
        context_data = curs.fetchall()

        return Classifier._filter_out_empty_entities(query_data, context_data)

    @staticmethod
    def _filter_out_empty_entities(query_data: List[sqlite3.Row], context_data: List[sqlite3.Row]
                                   ) -> Tuple[List[sqlite3.Row], List[sqlite3.Row]]:
        """
        Due to additional filtering of trivial samples (optional) or the ensuring that the query and context split only
        have a disjoint set of sentences as samples, it is possible that entities are left with either 0 query or
        context sentences. These entities can't be used for the context based classifiers, so they have to be
        filtered out manually here.
        """
        query_entities = set([x['entity_title'] for x in query_data])
        context_entities = set([x['entity_title'] for x in context_data])
        trivial_entities = query_entities ^ context_entities

        filtered_query_data = [sample for sample in query_data if sample['entity_title'] not in trivial_entities]
        filtered_context_data = [sample for sample in context_data if sample['entity_title'] not in trivial_entities]

        filtered_query_entities = set([x['entity_title'] for x in filtered_query_data])
        filtered_context_entities = set([x['entity_title'] for x in filtered_context_data])
        assert filtered_query_entities == filtered_context_entities, "The filtered context and query samples do not " \
                                                                     "share the same entities"

        return filtered_query_data, filtered_context_data

    @staticmethod
    def _connect_db(db_name: str, timeout: float = 300.0) -> Tuple[sqlite3.Cursor, sqlite3.Connection]:
        connection = sqlite3.connect(db_name, timeout=timeout)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA synchronous = OFF")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("BEGIN TRANSACTION")
        curs = connection.cursor()

        return curs, connection

    @staticmethod
    def _close_db(connection: sqlite3.Connection):
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

            suggestions = self._classify(mention, sentence=sentence, num_results=num_results)

            # FIXME: comment out, only relevant for debugging purposes to check nn sentences and missed sentences
            self._debug_info(suggestions, entity, mention, sentence)

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

    def _debug_info(self, suggestions, entity, mention, sentence):
        """
            Only used to print out nearest neighbors and some special cases for the bert based classifier.
        """
        nn_sentences = suggestions.get('nn_sentences', None)
        if nn_sentences[0][0] != entity:
            # Case: the GT entity is not in the top n results at all
            if entity not in [e[0] for e in nn_sentences]:
                print("FP* | entity: %s | mention: %s | sentence: %s" % (entity, mention, sentence))
            # Case: the GT entity is somewhere in the top n results but not the first suggestion
            else:
                print("FP | entity: %s | mention: %s | sentence: %s" % (entity, mention, sentence))
        else:
            print("TP | entity: %s | mention: %s | sentence: %s" % (entity, mention, sentence))

        # Print out sentences that were relevant for the current sample but missed
        relevant_context_data = [context_sample for context_sample in self._context_data if
                                 context_sample['entity_title'] == entity]

        # In order to get the mention for a suggestion sentence I need to check every context sentence again
        for nn_sample in nn_sentences:
            for context_sample in self._context_data:
                if (nn_sample[0], nn_sample[2]) == (context_sample['entity_title'], context_sample['sentence']):
                    print("entity: %s | score: %0.5f | mention: %s | sentence: %s" % (nn_sample[0], nn_sample[1], context_sample['mention'], nn_sample[2]))

        trivial_missed_context_sentences = []
        difficult_missed_context_sentences = []
        for context_sample in relevant_context_data:
            if ((str(entity), context_sample['sentence']) not in
                    [(str(nn_sample[0]), nn_sample[2]) for nn_sample in nn_sentences]):
                if str(context_sample['mention']) != str(mention).replace("_", " "):
                    difficult_missed_context_sentences.append(context_sample)
                else:
                    trivial_missed_context_sentences.append(context_sample)

        print("\nTrivial missed context sentences (query sentence mention == context sentence mention): ")
        for sample in trivial_missed_context_sentences:
            print("mention: %s | sentence: %s" % (sample['mention'], sample['sentence']))

        print("\nDifficult missed context sentences (query sentence mention != context sentence mention): ")
        for sample in difficult_missed_context_sentences:
            print("mention: %s | sentence: %s" % (sample['mention'], sample['sentence']))
        print("\n\n")
