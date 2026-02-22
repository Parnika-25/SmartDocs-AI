import uuid
import math
import re
import tiktoken


class TextChunker:
    """
    Handles text chunking using:
    1. Fixed token-based chunking with overlap
    2. Sentence-based semantic chunking
    """

    def __init__(self, model_name="gpt-3.5-turbo"):
        self.encoder = tiktoken.encoding_for_model(model_name)

    # --------------------------------------------------
    # Utility Functions
    # --------------------------------------------------
    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def calculate_optimal_chunk_size(self, text: str) -> int:
        """
        Dynamically calculate chunk size based on document length
        """
        total_tokens = self.count_tokens(text)

        if total_tokens < 3000:
            return 500
        elif total_tokens < 10000:
            return 800
        else:
            return 1000

    def merge_small_chunks(self, chunks, min_tokens=200):
        """
        Merge chunks that are too small with neighboring chunks
        """
        merged = []
        buffer = ""

        for chunk in chunks:
            if self.count_tokens(buffer) < min_tokens:
                buffer += " " + chunk["text"]
            else:
                merged.append(buffer.strip())
                buffer = chunk["text"]

        if buffer:
            merged.append(buffer.strip())

        return merged

    # --------------------------------------------------
    # Chunking Strategies
    # --------------------------------------------------
    def chunk_by_tokens(
        self,
        text: str,
        source_file: str,
        page_number: int,
        chunk_size=1000,
        overlap=200
    ):
        """
        Fixed-size token chunking with overlap
        """
        tokens = self.encoder.encode(text)
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(tokens):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoder.decode(chunk_tokens)

            chunk_data = {
                "chunk_id": str(uuid.uuid4()),
                "chunk_index": chunk_index,
                "text": chunk_text,
                "source_file": source_file,
                "page_number": page_number,
                "token_count": len(chunk_tokens),
                "char_count": len(chunk_text),
                "word_count": len(chunk_text.split())
            }

            chunks.append(chunk_data)

            start += chunk_size - overlap
            chunk_index += 1

        return chunks

    def chunk_by_sentences(
        self,
        text: str,
        source_file: str,
        page_number: int,
        max_tokens=1000,
        overlap_tokens=200
    ):
        """
        Sentence-aware chunking that preserves semantic boundaries
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        current_tokens = 0
        chunk_index = 0

        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)

            if current_tokens + sentence_tokens <= max_tokens:
                current_chunk += " " + sentence
                current_tokens += sentence_tokens
            else:
                # Save current chunk
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "chunk_index": chunk_index,
                    "text": current_chunk.strip(),
                    "source_file": source_file,
                    "page_number": page_number,
                    "token_count": current_tokens,
                    "char_count": len(current_chunk),
                    "word_count": len(current_chunk.split())
                })

                # Start new chunk with overlap
                overlap_text = current_chunk.split()[-overlap_tokens:]
                current_chunk = " ".join(overlap_text) + " " + sentence
                current_tokens = self.count_tokens(current_chunk)
                chunk_index += 1

        if current_chunk.strip():
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "chunk_index": chunk_index,
                "text": current_chunk.strip(),
                "source_file": source_file,
                "page_number": page_number,
                "token_count": current_tokens,
                "char_count": len(current_chunk),
                "word_count": len(current_chunk.split())
            })

        return chunks

    # --------------------------------------------------
    # Master Chunking Function
    # --------------------------------------------------
    def create_chunks(
        self,
        text: str,
        source_file: str,
        page_number: int,
        strategy="tokens"
    ):
        """
        Create chunks using selected strategy
        """
        if not text or not text.strip():
            return []

        optimal_size = self.calculate_optimal_chunk_size(text)

        if strategy == "sentences":
            return self.chunk_by_sentences(
                text,
                source_file,
                page_number,
                max_tokens=optimal_size
            )

        return self.chunk_by_tokens(
            text,
            source_file,
            page_number,
            chunk_size=optimal_size
        )
