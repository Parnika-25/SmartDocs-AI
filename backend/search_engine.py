# import math, json, os
# from collections import Counter
# from backend.embeddings import EmbeddingGenerator
# from backend.vector_db import VectorDatabase
# from utils.error_handler import EmbeddingError, DatabaseError, logger

# CACHE_FILE = "cache/search_cache.json"
# os.makedirs("cache", exist_ok=True)


# class SearchEngine:

#     def __init__(self):
#         self.embedder = EmbeddingGenerator()
#         self.db = VectorDatabase()
#         self.collection = self.db.create_collection()

#     def cosine(self, v1, v2):
#         dot = sum(a*b for a,b in zip(v1,v2))
#         n1 = math.sqrt(sum(a*a for a in v1))
#         n2 = math.sqrt(sum(b*b for b in v2))
#         return dot / (n1*n2) if n1 and n2 else 0

#     def search_similar_chunks(self, query: str, user: str, k=8):
#         try:
#             q_emb = self.embedder.generate_embedding(query)
#         except:
#             raise EmbeddingError("Embedding failed")

#         try:
#             res = self.collection.query(
#                 query_embeddings=[q_emb],
#                 n_results=k,
#                 include=["documents","metadatas","embeddings"]
#             )
#         except:
#             raise DatabaseError("DB unavailable")

#         results = []
#         for d,m,e,i in zip(res["documents"][0],res["metadatas"][0],res["embeddings"][0],res["ids"][0]):
#             score = self.cosine(q_emb, e)
#             results.append({
#                 "chunk_text": d,
#                 "source_file": m["source_file"],
#                 "page_number": m["page_number"],
#                 "relevance_score": round(score,4)
#             })

#         self._cache(query, results)
#         return sorted(results, key=lambda x:x["relevance_score"], reverse=True)

#     def keyword_search(self, query, k=8):
#         logger.warning("Using keyword fallback")
#         try:
#             docs = self.collection.get(include=["documents","metadatas"])
#         except:
#             return []

#         scored=[]
#         for d,m in zip(docs["documents"],docs["metadatas"]):
#             score = sum(1 for w in query.lower().split() if w in d.lower())
#             if score:
#                 scored.append({
#                     "chunk_text": d,
#                     "source_file": m["source_file"],
#                     "page_number": m["page_number"],
#                     "relevance_score": score
#                 })
#         return sorted(scored, key=lambda x:x["relevance_score"], reverse=True)[:k]

#     def load_cached_results(self, query):
#         if not os.path.exists(CACHE_FILE):
#             return []
#         with open(CACHE_FILE) as f:
#             return json.load(f).get(query, [])

#     def _cache(self, query, results):
#         data={}
#         if os.path.exists(CACHE_FILE):
#             with open(CACHE_FILE) as f:
#                 data=json.load(f)
#         data[query]=results
#         with open(CACHE_FILE,"w") as f:
#             json.dump(data,f)
import math
import json
import os
import logging

from backend.embeddings import EmbeddingGenerator
from backend.vector_db import VectorDatabase
from utils.error_handler import EmbeddingError, DatabaseError

logger = logging.getLogger(__name__)

CACHE_FILE = "cache/search_cache.json"
os.makedirs("cache", exist_ok=True)


class SearchEngine:
    """
    SearchEngine performs vector similarity search
    against a USER-SPECIFIC ChromaDB collection.
    """

    def __init__(self, user: str):
        self.user = user
        self.embedder = EmbeddingGenerator()

        # 🔥 IMPORTANT: must match DocumentIngestion collection name
        collection_name = f"user_{user.replace(' ', '_')}"
        self.db = VectorDatabase(collection_name=collection_name)
        self.collection = self.db.create_collection()

    # ---------------------------
    # Utility: cosine similarity
    # ---------------------------
    def cosine(self, v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a * a for a in v1))
        n2 = math.sqrt(sum(b * b for b in v2))
        return dot / (n1 * n2) if n1 and n2 else 0

    # -------------------------------------------------
    # VECTOR SEARCH (MAIN METHOD)
    # -------------------------------------------------
    def search_similar_chunks(self, query: str, k: int = 8):
        """
        Perform vector similarity search for the given query.
        Uses the user's private collection.
        """

        # 1️⃣ Generate query embedding
        try:
            q_emb = self.embedder.generate_embedding(query)
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise EmbeddingError("Embedding failed")

        # 2️⃣ Query ChromaDB (NO user filter needed)
        try:
            res = self.collection.query(
                query_embeddings=[q_emb],
                n_results=k,
                include=["documents", "metadatas", "embeddings"]
            )
        except Exception as e:
            logger.error(f"Vector DB query failed: {e}")
            raise DatabaseError("DB unavailable")

        # 3️⃣ Handle empty results
        if not res or not res.get("documents") or not res["documents"][0]:
            logger.warning(
                f"No chunks retrieved for user='{self.user}', query='{query}'"
            )
            return []

        # 4️⃣ Rank results by cosine similarity
        results = []
        for doc, meta, emb in zip(
            res["documents"][0],
            res["metadatas"][0],
            res["embeddings"][0]
        ):
            score = self.cosine(q_emb, emb)
            results.append({
                "chunk_text": doc,
                "source_file": meta.get("source_file", "Unknown"),
                "page_number": meta.get("page_number", "?"),
                "relevance_score": round(score, 4)
            })

        results = sorted(results, key=lambda x: x["relevance_score"], reverse=True)

        logger.info(f"[SEARCH] user={self.user}, results={len(results)}")

        # Optional caching
        self._cache(query, results)

        return results

    # -------------------------------------------------
    # OPTIONAL: CACHE
    # -------------------------------------------------
    def _cache(self, query: str, results):
        try:
            data = {}
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as f:
                    data = json.load(f)

            data[f"{self.user}:{query}"] = results

            with open(CACHE_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            # Cache failure should NEVER break search
            pass
