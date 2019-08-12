from abc import ABCMeta, abstractmethod
from typing import Tuple, List, Set, Dict, Union
import sqlite3
import datetime
import spacy
import json
import re
import numpy as np
from collections import OrderedDict

from eval.evaluation import Evaluator


class Classifier(metaclass=ABCMeta):
    def __init__(self, dataset_db_name: str, dataset_split: str, split_table_name: str='splits',
                 skip_trivial_samples: bool = False, load_context: bool = False, query_data=None,
                 context_data=None, entities=None, loaded_datasplit=None):
        self._loaded_datasplit = None
        self._query_data = None
        self._context_data = None
        self._mention_entity_duplicate_count = {}
        self._entities = None
        self._nlp = spacy.load('de_core_news_sm')

        self._dataset_db_name = dataset_db_name
        self._split_table_name = split_table_name
        self._skip_trivial_samples = skip_trivial_samples

        self._dates_regex = re.compile(r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$')
        self._email_regex = re.compile(r'\b\w+\.?\w*@\w+[-,_]?\w*\b')

        # Load the specified datasplit
        assert dataset_split in ['train', 'test', 'val'], "The datasplit is not valid."
        if (query_data is not None and context_data is not None and entities is not None and
                loaded_datasplit is not None):
            self.set_data(query_data, context_data, entities, loaded_datasplit)
        else:
            self._query_data, self._context_data, self._entities, self._loaded_datasplit = Classifier.load_datasplit(
                dataset_db_name, dataset_split, split_table_name=split_table_name,
                skip_trivial_samples=skip_trivial_samples, load_context=load_context)

    def set_data(self, query_data, context_data, entities, loaded_datasplit):
        assert loaded_datasplit in ['train', 'test', 'val'], "The datasplit is not valid."
        self._query_data = query_data
        self._context_data = context_data
        self._entities = entities
        self._loaded_datasplit = loaded_datasplit

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
        _entities = set([x['entity_title'] for x in _context_data])
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
            AND (
                    (
                    LENGTH(trim(sentences.mention)) > 0
                    AND instr(sentences.sentence, trim(sentences.mention)) > 0
                    AND sentences.sentence NOT IN (
                        SELECT tmp.sentence
                        FROM sentences as tmp
                        INNER JOIN %s
                            ON %s.sample_id = tmp.rowid
                        WHERE (%s.data_split = ? or %s.data_split = ?)
                        )
                    )
                    OR 
                    (
                    sentences.backlink_id=-1
                    AND
                        (
                        instr(sentences.sentence, trim(sentences.mention)) > 0
                        OR
                        sentences.mention='[NIL]'
                        )
                    )
                )
            
        """ % (split_table_name, split_table_name, split_table_name, split_table_name, split_table_name, split_table_name, split_table_name, split_table_name)
        command_skip_trivial_samples = """
            AND LOWER(REPLACE(sentences.mention, '_', ' ')) != LOWER(REPLACE(entity_title, '_', ' '))
        """

        # Note: The backlink_id is only set for Wikipedia datasets.
        # For the empolis dataset this can be used to disable the filtering automatically
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
                AND sentences.backlink_id!=-1
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

        # Don't filter if we are using empolis data where the query samples don't have a GT entity
        if len(query_entities) == 1 and list(query_entities)[0] == "[NIL]":
            return query_data, context_data
        else:
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
    def _classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]", num_results: int=1) -> \
            Union[Dict[str, Dict[str, Union[float, int]]], List[Tuple[str, Dict[str, Dict[str, Union[float, int]]]]]]:
        """
        Internal classify method that collects raw results that might be interesting for statistics.
        """
        pass

    @abstractmethod
    def classify(self, mentions: Union[str, List[str]]="[NIL]", sentence: str="[NIL]") -> Union[Set[str], List[Tuple[str, Set[str]]]]:
        """
        Public classify method that users can use to classify a given string including some sort of similarity measure.
        """
        pass

    def _identify_potential_mentions(self, sentence: str) -> List[str]:
        """
        Identify potential mentions in a sentence.
        """
        potential_mentions = [str(w) for w in self._nlp(sentence) if w.pos_ in ['NOUN', 'PROPN']]

        # Remove mentions that are composed of only one char or are far too long to be a word
        potential_mentions = [w for w in potential_mentions if len(str(w)) > 1 or len(str(w)) > 40]

        common_words = ["mm", "ca", "d.h.", "cm", "z.b.", "grad", "ok", ]

        # Remove common words
        potential_mentions = [w for w in potential_mentions if str(w).lower() not in common_words]

        # Remove dates
        potential_mentions = [i for i in potential_mentions if not self._dates_regex.search(i)]

        # Remove emails
        potential_mentions = [i for i in potential_mentions if not self._email_regex.search(i)]

        # print(potential_mentions)
        return potential_mentions

    @staticmethod
    def _add_suggestion_to_eval_results(suggestions, sample, eval_results):
        entity = sample['entity_title']
        mention = sample['mention']

        # FIXME: comment out, only relevant for debugging purposes to check nn sentences and missed sentences
        # self._debug_info(suggestions, entity, mention, sentence)

        if 'sentence' not in suggestions:
            suggestions['sentence'] = sample['sentence']

        if entity not in eval_results:
            eval_results[entity] = {}

        if mention not in eval_results[entity]:
            eval_results[entity][mention] = []

        eval_results[entity][mention].append(suggestions)

        return eval_results

    def _evaluate_empolis(self, suggestions, sample, empolis_mapping, eval_results, empolis_distance_threshold):
        for suggestion in suggestions:
            mention = str(suggestion[0]).strip()
            gt_entity_data = empolis_mapping.get(mention, None)

            # If the mention is known in the empolis data and part of the query split, add it to the eval results
            if gt_entity_data is not None and gt_entity_data['query_context_split'] == 'query':
                updated_sample = {
                    'sentence': sample['sentence'],
                    'mention': mention,
                    'entity_title': gt_entity_data['entities'][0]
                }

                # If the GT entity is not part of the current split, ignore it
                if updated_sample['entity_title'] in self._entities:
                    eval_results = self._add_suggestion_to_eval_results(suggestion[1], updated_sample, eval_results)

            # Otherwise, if the classifier suggests something just print it
            elif gt_entity_data is None and len(suggestion[1]['suggestions']) > 0:
                tmp_str = ""
                for s, score in suggestion[1]['suggestions'].items():
                    # Only suggest entities if the classifier is certain
                    if score <= empolis_distance_threshold:
                        tmp_str = tmp_str + "; " + str(s) + " : " + str(score)

                if len(tmp_str) > 0:
                    print("Found the following suggestion(s) for the unknown mention '%s': %s" %
                          (suggestion[0], tmp_str))
                    print(sample['sentence'])
                    print("------------------------------------------------------------------------------")
            # All other cases are ignored/skipped
            else:
                pass

        return eval_results

    @abstractmethod
    def evaluate_datasplit(self, split: str, num_results: int = 1, eval_mode: str= 'mentions',
                           empolis_mapping_path: str=None, empolis_distance_threshold: float=0.85):
        """
        Evaluate the given datasplit.
        split has to be one of the three: train, test, val.
        """
        assert split in ['train', 'test', 'val'], "The given evaluation split is not a valid split."
        assert split == self._loaded_datasplit, "The evaluation split has not been loaded."

        assert eval_mode in ['mentions', 'samples'], "The evaluation mode is not a valid mode."
        start = datetime.datetime.now()

        empolis_mapping = None
        if empolis_mapping_path is not None:
            with open(empolis_mapping_path, 'r') as f:
                empolis_mapping = json.load(f)

        eval_results = {}
        for sample in self._query_data:
            sentence = sample['sentence']
            mention = sample['mention']

            suggestions = self._classify(mention, sentence=sentence, num_results=num_results)
            if mention == "[NIL]" and empolis_mapping is not None:
                eval_results = self._evaluate_empolis(suggestions, sample, empolis_mapping, eval_results,
                                                      empolis_distance_threshold)
            elif mention != "[NIL]":
                eval_results = self._add_suggestion_to_eval_results(suggestions, sample, eval_results)

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

    # @abstractmethod
    def evaluate_potential_synonyms(self, empolis_mapping_path: str, distance_threshold: float=0.85):
        """
        Evaluates how well a classifier is able to predict synonyms for the entities of a dataset.
        This has to be done using a different evaluation method because it does not evaluate whether a classifier
        is able to predict a mention correctly but rather whether a classifier is able to predict all synonyms/mentions
        for the Empolis dataset that are known for an entity.

        Because this is a completely different kind of evaluation a separate method has been implemented.
        """
        with open(empolis_mapping_path, 'r') as f:
            empolis_mapping_synonym_to_entity = json.load(f)

        # Remove all entries that are not part of the current split, because they can't be predicted by the
        # classifier and therefore should not be used for the evaluation
        synonyms_to_remove = []
        for synonym, entity_data in empolis_mapping_synonym_to_entity.items():
            if entity_data['entities'][0] not in self._entities:
                synonyms_to_remove.append(synonym)

        for synonym in synonyms_to_remove:
            del empolis_mapping_synonym_to_entity[synonym]

        # Classify all query samples
        res, identified_mentions = self._get_potential_synonyms(distance_threshold=distance_threshold)
        relevant_synonyms = {}
        for mention in identified_mentions:
            # Check if the mention is known to the Empolis dataset
            ground_truth_entity = empolis_mapping_synonym_to_entity.get(mention, None)
            if ground_truth_entity is not None:
                ground_truth_entity = ground_truth_entity['entities'][0]

                # If it is known, mark it accordingly for all mentions for the respective entity
                if ground_truth_entity not in relevant_synonyms:
                    relevant_synonyms[ground_truth_entity] = set([mention])
                else:
                    relevant_synonyms[ground_truth_entity].update([mention])
            else:
                # Remove all mentions that are not relevant for the evaluation (aka not known to the empolis data)
                for entity in res.keys():
                    if mention in res[entity]:
                        del res[entity][mention]

        # Evaluation
        evaluator = Evaluator()
        _, macro, micro = evaluator.evaluate_empolis_synonyms(res, relevant_synonyms)

        # Note: the top1 accuracy is not relevant here because we have no top x evaluation here
        print("\nMacro metrics:"
              "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % macro)
        print("\nMicro metrics:"
              "\nPrecision: %.2f%%, Recall: %.2f%%, F1-Score: %.2f%%" % micro)

    @abstractmethod
    def _get_potential_synonyms(self, distance_threshold=0.85):
        """
        Identify potential synonyms in all query sentences and return a dictionary for every entity that is known
        to the classifier with a ranked list of potential synonyms.
        """
        res = {}
        identified_mentions = set()
        for sample in self._query_data:
            sentence = sample['sentence']

            suggestions = self._classify(sentence=sentence, num_results=1)
            for mention, s in suggestions:
                # This part is only necessary for the evaluation, so that the classifier knows which synonyms
                # actually appeared in the text
                identified_mentions.update([mention])

                for suggested_entity, distances in s['suggestions'].items():
                    # Filter out every suggestion that does not meet the distance requirement
                    # if np.average(distances) > distance_threshold:
                    if np.min(distances) > distance_threshold:
                        continue

                    # Store the classification result
                    if suggested_entity not in res:
                        res[suggested_entity] = {mention: {
                            'distances': [distances],
                            'sentences': [sentence]
                        }}
                    else:
                        if mention not in res[suggested_entity]:
                            res[suggested_entity][mention] = {
                                'distances': [distances],
                                'sentences': [sentence]
                            }
                        else:
                            res[suggested_entity][mention]['distances'].append(distances)
                            res[suggested_entity][mention]['sentences'].append(sentence)

        # Resort everything
        for e in res.keys():
            res[e] = OrderedDict(sorted(res[e].items(), key=lambda item: np.average(item[1]['distances'])))

        return res, identified_mentions

    def get_potential_synonyms(self, entity: str, distance_threshold=0.85):
        """
        Public method to extract potential synonyms for a single given entity.
        """
        res, _ = self._get_potential_synonyms(distance_threshold=distance_threshold)

        # for entity, entity_data in res.items():
        #     print(entity, entity_data)
        #     print("-----------------------------")

        return res.get(entity, {})

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
