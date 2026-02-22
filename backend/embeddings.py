import time
import json
import hashlib
from datetime import datetime
import openai
from dotenv import load_dotenv
import os


class EmbeddingGenerator:
    """
    Generates embeddings for text chunks using OpenAI embedding model.
    Implements:
    - single embedding
    - batch embeddings
    - caching
    - retry with exponential backoff
    - rate limiting (60 req/min)
    """

    def __init__(self, model_name="text-embedding-ada-002", cache_path="data/embedding_cache.json"):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found in .env")

        openai.api_key = api_key
        self.model_name = model_name
        self.cache_path = cache_path
        self.cache = self._load_cache()

    # -------------------------
    # Cache Helpers
    # -------------------------
    def _load_cache(self):
        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception:
            return {}

    def _save_cache(self):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f)

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    # -------------------------
    # Rate Limit Delay
    # -------------------------
    def add_delay(self, seconds=1):
        """
        Adds delay between API requests to respect rate limits.
        """
        time.sleep(seconds)

    # -------------------------
    # Retry Logic
    # -------------------------
    def _retry_request(self, func, retries=3):
        """
        Retry wrapper with exponential backoff:
        wait times -> 1s, 2s, 4s
        """
        delay = 1
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                if attempt == retries - 1:
                    raise RuntimeError(f"API request failed after {retries} attempts: {e}")
                time.sleep(delay)
                delay *= 2

    # -------------------------
    # Embedding Generation
    # -------------------------
    def generate_embedding(self, text: str):
        """
        Generate single embedding vector for text.
        Uses caching to avoid regenerating.
        """
        if not text or not text.strip():
            raise ValueError("Text is empty, cannot generate embedding")

        text_key = self._hash_text(text.strip())

        # Return cached embedding if exists
        if text_key in self.cache:
            return self.cache[text_key]

        def api_call():
            return openai.Embedding.create(
                model=self.model_name,
                input=text
            )

        response = self._retry_request(api_call)
        embedding = response["data"][0]["embedding"]

        # Dimension verification
        if len(embedding) != 1536:
            raise RuntimeError(f"Embedding dimension mismatch: expected 1536, got {len(embedding)}")

        # Save in cache
        self.cache[text_key] = embedding
        self._save_cache()

        return embedding

    def generate_batch_embeddings(self, chunks, max_requests_per_minute=60):
        """
        Generate embeddings for multiple chunks with rate limiting.
        Each chunk must contain "text".
        """

        results = []
        delay_seconds = 60 / max_requests_per_minute  # ~1 sec per request

        for chunk in chunks:
            text = chunk.get("text", "")

            embedding = self.generate_embedding(text)

            results.append({
                "chunk": chunk,
                "embedding": embedding
            })

            # Rate limit delay
            self.add_delay(seconds=delay_seconds)

        return results

    # -------------------------
    # Prepare Embedding Data Output
    # -------------------------
    def prepare_embedding_data(self, embedded_chunks):
        """
        Convert embedded chunks into final structured output
        """
        final_data = []

        for item in embedded_chunks:
            chunk = item["chunk"]
            embedding = item["embedding"]

            # Dimension check again
            if len(embedding) != 1536:
                raise RuntimeError("Invalid embedding dimension during prepare step")

            final_data.append({
                "embedding_vector": embedding,
                "text": chunk.get("text", ""),
                "metadata": {
                    "chunk_id": chunk.get("chunk_id"),
                    "chunk_index": chunk.get("chunk_index"),
                    "source_file": chunk.get("source_file"),
                    "page_number": chunk.get("page_number"),
                    "token_count": chunk.get("token_count"),
                    "word_count": chunk.get("word_count"),
                    "char_count": chunk.get("char_count")
                },
                "timestamp": datetime.utcnow().isoformat()
            })

        return final_data
