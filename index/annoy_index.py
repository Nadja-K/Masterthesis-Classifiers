import annoy
import lmdb
import sent2vec

from pathlib import Path
from typing import Set, List


class AnnoyIndexer:
    def __init__(self, embedding_model_path: str, embedding_model_type: str):
        self._annoy_index = None
        self._annoy_mapping = None

        assert embedding_model_type in ['sent2vec']
        self._embedding_model_type = embedding_model_type
        if self._embedding_model_type == 'sent2vec':
            self._embedding_model = sent2vec.Sent2vecModel()
            self._embedding_model.load_model(embedding_model_path)
            self._embedding_vector_size = self._embedding_model.get_emb_size()

    def create_entity_index(self, entities: Set[str], output_filename: str, num_trees: int=30):
        file_annoy = output_filename + ".ann"
        file_lmdb = output_filename + ".lmdb"

        # Create AnnoyIndex instance
        self._annoy_index = annoy.AnnoyIndex(self._embedding_vector_size)

        # Create mapping instance
        self._annoy_mapping = lmdb.open(file_lmdb, map_size=int(1e9))

        # Get (sent2vec) embeddings for all entities
        with self._annoy_mapping.begin(write=True) as mapping:
            for entity_id, entity in enumerate(entities):
                # Replace _ symbols with spaces
                entity = str(entity)
                refactored_entity = entity.replace("_", " ")

                if self._embedding_model_type == 'sent2vec':
                    emb = self._embedding_model.embed_sentence(refactored_entity)[0]

                # Add entity embedding to index
                self._annoy_index.add_item(entity_id, emb)

                # Add ID <-> word mapping
                mapping.put(str(entity_id).encode(), entity.encode())
                print(entity, entity_id)

        # Build annoy index
        self._annoy_index.build(num_trees)

        # Save annoy index
        self._annoy_index.save(file_annoy)

    def load_entity_index(self, file_annoy: str):
        """
        Load an annoy index and the corresponding lmdb mapping.

        :param file_annoy: 'path/filename.ann'
        """
        file_lmdb = ".".join(file_annoy.split(".")[:-1]) + ".lmdb"
        assert Path(file_annoy).is_file(), "The annoy file could not be found. Make sure the path is correct."
        assert Path(file_lmdb).is_file(), "The lmdb mapping could not be found. Make sure it is in the same " \
                                          "directory as the .ann file and has the same file name except for " \
                                          "the file extension (.lmdb)."

        self._annoy_index = annoy.AnnoyIndex(self._embedding_vector_size)
        self._annoy_index.load(file_annoy)

        self._annoy_mapping = lmdb.open(file_lmdb, map_size=int(1e9))

    def get_nns_by_vector(self, emb_vector: List[float], num_nn: int) -> Set[str]:
        """
        Returns a set of nearest neighbour entities for the given embedding vector.
        """
        assert self._annoy_index is not None, "No annoy index has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_mapping is not None, "No annoy mapping has been loaded. Call load_entity_index(file_annoy)"

        nns_ids = self._annoy_index.get_nns_by_vector(emb_vector, num_nn)
        nns_entities = set()
        with self._annoy_mapping.begin() as mapping:
            for id in nns_ids:
                nns_entities.add(mapping.get(str(id).encode()).decode())

        return nns_entities

    def get_nns_by_phrase(self, phrase: str, num_nn: int) -> Set[str]:
        """
        Returns a set of nearest neighbour entities for the given phrase.
        """
        assert self._annoy_index is not None, "No annoy index has been loaded. Call load_entity_index(file_annoy)"
        assert self._annoy_mapping is not None, "No annoy mapping has been loaded. Call load_entity_index(file_annoy)"

        phrase = str(phrase)
        refactored_phrase = phrase.replace("_", " ")

        nns_entities = set()
        if self._embedding_model_type == 'sent2vec':
            emb = self._embedding_model.embed_sentence(refactored_phrase)[0]
            nns_entities = self.get_nns_by_vector(emb, num_nn)

        return nns_entities
