# import os
# import chromadb
# from chromadb.config import Settings


# class VectorDatabase:
#     """
#     VectorDatabase manages ChromaDB persistent client and collection CRUD operations.
#     """

#     def __init__(self, persist_dir="data/chroma_db", collection_name="smartdocs_collection"):
#         self.persist_dir = persist_dir
#         self.collection_name = collection_name

#         os.makedirs(self.persist_dir, exist_ok=True)

#         try:
#             self.client = chromadb.PersistentClient(path=self.persist_dir)
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to connect to ChromaDB: {e}")

#     # -------------------------------------------------
#     # Connection Verification
#     # -------------------------------------------------
#     def verify_connection(self):
#         """
#         Simple check to verify ChromaDB client works
#         """
#         try:
#             _ = self.client.list_collections()
#             return True
#         except Exception as e:
#             raise RuntimeError(f"❌ ChromaDB connection verification failed: {e}")

#     # -------------------------------------------------
#     # Collection Helpers
#     # -------------------------------------------------
#     def check_collection_exists(self) -> bool:
#         """
#         Check if collection already exists
#         """
#         try:
#             collections = self.client.list_collections()
#             return any(col.name == self.collection_name for col in collections)
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to check collection existence: {e}")

#     def create_collection(self):
#         """
#         Create or load collection with name smartdocs_collection
#         """
#         try:
#             collection = self.client.get_or_create_collection(
#                 name=self.collection_name,
#                 metadata={"description": "SmartDocs AI Embeddings Collection"}
#             )
#             return collection
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to create/load collection: {e}")

#     def delete_collection(self):
#         """
#         Delete entire collection
#         """
#         try:
#             if self.check_collection_exists():
#                 self.client.delete_collection(self.collection_name)
#                 return True
#             return False
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to delete collection: {e}")

#     # -------------------------------------------------
#     # CRUD Operations
#     # -------------------------------------------------
#     def add_documents(self, ids, embeddings, documents, metadatas):
#         """
#         Insert embeddings with schema:
#         ids -> unique IDs
#         embeddings -> vector list
#         documents -> text chunks
#         metadatas -> {source_file, page_number, chunk_id}
#         """
#         try:
#             collection = self.create_collection()

#             collection.add(
#                 ids=ids,
#                 embeddings=embeddings,
#                 documents=documents,
#                 metadatas=metadatas
#             )
#             return True
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to add documents: {e}")

#     def update_document(self, doc_id, embedding=None, document=None, metadata=None):
#         """
#         Update an existing embedding/document/metadata by ID.
#         """
#         try:
#             collection = self.create_collection()

#             update_data = {"ids": [doc_id]}

#             if embedding is not None:
#                 update_data["embeddings"] = [embedding]

#             if document is not None:
#                 update_data["documents"] = [document]

#             if metadata is not None:
#                 update_data["metadatas"] = [metadata]

#             collection.update(**update_data)
#             return True
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to update document: {e}")

#     def get_collection_stats(self):
#         """
#         Return collection stats like count and metadata
#         """
#         try:
#             if not self.check_collection_exists():
#                 return {
#                     "collection_name": self.collection_name,
#                     "exists": False,
#                     "total_documents": 0
#                 }

#             collection = self.create_collection()
#             return {
#                 "collection_name": self.collection_name,
#                 "exists": True,
#                 "total_documents": collection.count(),
#                 "metadata": collection.metadata
#             }
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to get collection stats: {e}")

#     def get_all_documents(self, limit=10):
#         """
#         Retrieve stored documents (for testing)
#         """
#         try:
#             collection = self.create_collection()
#             results = collection.get(limit=limit, include=["documents", "embeddings", "metadatas"])
#             return results
#         except Exception as e:
#             raise RuntimeError(f"❌ Failed to fetch documents: {e}")

import os
import chromadb
from chromadb.config import Settings


class VectorDatabase:
    """
    VectorDatabase manages ChromaDB persistent client and collection CRUD operations.
    """

    def __init__(self, persist_dir="data/chroma_db", collection_name="smartdocs_collection"):
        self.persist_dir = persist_dir
        self.collection_name = collection_name

        os.makedirs(self.persist_dir, exist_ok=True)

        try:
            self.client = chromadb.PersistentClient(path=self.persist_dir)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to connect to ChromaDB: {e}")

    # -------------------------------------------------
    # Connection Verification
    # -------------------------------------------------
    def verify_connection(self):
        """
        Simple check to verify ChromaDB client works
        """
        try:
            _ = self.client.list_collections()
            return True
        except Exception as e:
            raise RuntimeError(f"❌ ChromaDB connection verification failed: {e}")

    # -------------------------------------------------
    # Collection Helpers
    # -------------------------------------------------
    def check_collection_exists(self) -> bool:
        """
        Check if collection already exists
        """
        try:
            collections = self.client.list_collections()
            return any(col.name == self.collection_name for col in collections)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to check collection existence: {e}")

    def create_collection(self):
        """
        Create or load collection with name smartdocs_collection
        """
        try:
            collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "SmartDocs AI Embeddings Collection"}
            )
            return collection
        except Exception as e:
            raise RuntimeError(f"❌ Failed to create/load collection: {e}")

    def delete_collection(self):
        """
        Delete entire collection
        """
        try:
            if self.check_collection_exists():
                self.client.delete_collection(self.collection_name)
                return True
            return False
        except Exception as e:
            raise RuntimeError(f"❌ Failed to delete collection: {e}")

    # -------------------------------------------------
    # CRUD Operations
    # -------------------------------------------------
    def add_documents(self, ids, embeddings, documents, metadatas):
        """
        Insert embeddings with schema:
        ids -> unique IDs
        embeddings -> vector list
        documents -> text chunks
        metadatas -> {source_file, page_number, chunk_id}
        """
        try:
            collection = self.create_collection()

            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            return True
        except Exception as e:
            raise RuntimeError(f"❌ Failed to add documents: {e}")

    def update_document(self, doc_id, embedding=None, document=None, metadata=None):
        """
        Update an existing embedding/document/metadata by ID.
        """
        try:
            collection = self.create_collection()

            update_data = {"ids": [doc_id]}

            if embedding is not None:
                update_data["embeddings"] = [embedding]

            if document is not None:
                update_data["documents"] = [document]

            if metadata is not None:
                update_data["metadatas"] = [metadata]

            collection.update(**update_data)
            return True
        except Exception as e:
            raise RuntimeError(f"❌ Failed to update document: {e}")

    def get_collection_stats(self):
        """
        Return collection stats like count and metadata
        """
        try:
            if not self.check_collection_exists():
                return {
                    "collection_name": self.collection_name,
                    "exists": False,
                    "total_documents": 0
                }

            collection = self.create_collection()
            return {
                "collection_name": self.collection_name,
                "exists": True,
                "total_documents": collection.count(),
                "metadata": collection.metadata
            }
        except Exception as e:
            raise RuntimeError(f"❌ Failed to get collection stats: {e}")

    def get_all_documents(self, limit=10):
        """
        Retrieve stored documents (for testing)
        """
        try:
            collection = self.create_collection()
            results = collection.get(limit=limit, include=["documents", "embeddings", "metadatas"])
            return results
        except Exception as e:
            raise RuntimeError(f"❌ Failed to fetch documents: {e}")