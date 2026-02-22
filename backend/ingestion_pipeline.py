# # import os
# # import time
# # import logging
# # from datetime import datetime

# # from backend.pdf_processor import PDFProcessor
# # from backend.text_cleaner import TextCleaner
# # from backend.text_chunker import TextChunker
# # from backend.embeddings import EmbeddingGenerator
# # from backend.vector_db import VectorDatabase

# # class DocumentIngestion:
# #     def __init__(self, collection_name="smartdocs_collection"):
# #         os.makedirs("logs", exist_ok=True)
# #         self.logger = logging.getLogger("DocumentIngestion")
# #         self.cleaner = TextCleaner()
# #         self.chunker = TextChunker()
# #         self.embedder = EmbeddingGenerator()
# #         self.vector_db = VectorDatabase(collection_name=collection_name)

# #     def process_single_document(self, pdf_path: str):
# #         # Extract the clean filename for metadata consistency
# #         source_file = os.path.basename(pdf_path)
# #         self.logger.info(f"Processing started for: {source_file}")
        
# #         processor = PDFProcessor(pdf_path)
# #         extracted_data = processor.extract_text_pymupdf()

# #         # Clean and Chunk logic
# #         cleaned_pages = {pg: self.cleaner.clean_text(txt) for pg, txt in extracted_data["text_by_page"].items()}
        
# #         all_chunks = []
# #         for page_number, cleaned_text in cleaned_pages.items():
# #             chunks = self.chunker.create_chunks(
# #                 text=cleaned_text,
# #                 source_file=source_file,
# #                 page_number=page_number,
# #                 strategy="sentences"
# #             )
# #             all_chunks.extend(chunks)

# #         # Generate Embeddings and store in ChromaDB
# #         embedded_chunks = self.embedder.generate_batch_embeddings(all_chunks)
# #         embedding_data = self.embedder.prepare_embedding_data(embedded_chunks)

# #         ids, embeddings, documents, metadatas = [], [], [], []
# #         for item in embedding_data:
# #             m = item["metadata"]
# #             ids.append(m["chunk_id"])
# #             embeddings.append(item["embedding_vector"])
# #             documents.append(item["text"])
# #             metadatas.append({
# #                 "source_file": source_file,
# #                 "page_number": m["page_number"],
# #                 "chunk_id": m["chunk_id"]
# #             })

# #         self.vector_db.add_documents(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
# #         return {"file_name": source_file, "status": "SUCCESS"}

# #     def process_multiple_documents(self, pdf_paths: list):
# #         return [self.process_single_document(path) for path in pdf_paths]

# import os
# import logging
# from backend.pdf_processor import PDFProcessor
# from backend.text_cleaner import TextCleaner
# from backend.text_chunker import TextChunker
# from backend.embeddings import EmbeddingGenerator
# from backend.vector_db import VectorDatabase

# class DocumentIngestion:
#     # ✅ Update: Accept 'user' and use it as the collection name
#     def __init__(self, user: str):
#         os.makedirs("logs", exist_ok=True)
#         self.logger = logging.getLogger("DocumentIngestion")
#         self.user = user
#         self.cleaner = TextCleaner()
#         self.chunker = TextChunker()
#         self.embedder = EmbeddingGenerator()
        
#         # ✅ Every user gets their own collection in the Vector DB
#         # ChromaDB collection names must be alphanumeric (no spaces)
#         collection_name = f"user_{user.replace(' ', '_')}"
#         self.vector_db = VectorDatabase(collection_name=collection_name)

#     def process_single_document(self, pdf_path: str):
#         source_file = os.path.basename(pdf_path)
#         self.logger.info(f"Processing started for: {source_file} (User: {self.user})")
        
#         try:
#             processor = PDFProcessor(pdf_path)
#             extracted_data = processor.extract_text_pymupdf()

#             cleaned_pages = {pg: self.cleaner.clean_text(txt) for pg, txt in extracted_data["text_by_page"].items()}
            
#             all_chunks = []
#             for page_number, cleaned_text in cleaned_pages.items():
#                 chunks = self.chunker.create_chunks(
#                     text=cleaned_text,
#                     source_file=source_file,
#                     page_number=page_number,
#                     strategy="sentences"
#                 )
#                 all_chunks.extend(chunks)

#             embedded_chunks = self.embedder.generate_batch_embeddings(all_chunks)
#             embedding_data = self.embedder.prepare_embedding_data(embedded_chunks)

#             ids, embeddings, documents, metadatas = [], [], [], []
#             for item in embedding_data:
#                 m = item["metadata"]
#                 ids.append(m["chunk_id"])
#                 embeddings.append(item["embedding_vector"])
#                 documents.append(item["text"])
#                 metadatas.append({
#                     "source_file": source_file,
#                     "page_number": m["page_number"],
#                     "chunk_id": m["chunk_id"],
#                     "user": self.user # ✅ Added user to metadata for safety
#                 })

#             self.vector_db.add_documents(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
#             return {"file_name": source_file, "status": "SUCCESS"}
            
#         except Exception as e:
#             self.logger.error(f"Failed to process {source_file}: {str(e)}")
#             raise e # Pass up to BatchProcessor

#     def process_multiple_documents(self, pdf_paths: list):
#         return [self.process_single_document(path) for path in pdf_paths]


import os
import logging

from backend.pdf_processor import PDFProcessor
from backend.text_cleaner import TextCleaner
from backend.text_chunker import TextChunker
from backend.embeddings import EmbeddingGenerator
from backend.vector_db import VectorDatabase

logger = logging.getLogger("DocumentIngestion")


class DocumentIngestion:
    """
    Handles PDF → text → chunks → embeddings → ChromaDB storage
    (per-user collection)
    """

    def __init__(self, user: str):
        os.makedirs("logs", exist_ok=True)
        self.user = user
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()
        self.embedder = EmbeddingGenerator()

        # 🔥 User-specific collection (MUST match SearchEngine)
        collection_name = f"user_{user.replace(' ', '_')}"
        self.vector_db = VectorDatabase(collection_name=collection_name)

        logger.info(f"Initialized ingestion for user={self.user}")

    def process_single_document(self, pdf_path: str):
        source_file = os.path.basename(pdf_path)
        logger.info(
            f"Processing started for: {source_file} (User: {self.user})"
        )

        try:
            # 1️⃣ Extract text
            processor = PDFProcessor(pdf_path)
            extracted_data = processor.extract_text_pymupdf()

            pages = extracted_data.get("text_by_page", {})
            logger.info(f"Pages extracted: {len(pages)}")

            # 2️⃣ Clean text
            cleaned_pages = {
                pg: self.cleaner.clean_text(txt)
                for pg, txt in pages.items()
                if txt and txt.strip()
            }

            # 3️⃣ Chunk text
            all_chunks = []
            for page_number, cleaned_text in cleaned_pages.items():
                chunks = self.chunker.create_chunks(
                    text=cleaned_text,
                    source_file=source_file,
                    page_number=page_number,
                    strategy="sentences"  # change to "paragraphs" if needed
                )
                all_chunks.extend(chunks)

            logger.info(f"Total chunks created: {len(all_chunks)}")

            if not all_chunks:
                logger.warning(
                    f"No chunks generated for {source_file} (User: {self.user})"
                )
                return {"file_name": source_file, "status": "NO_CHUNKS"}

            # 4️⃣ Generate embeddings
            embedded_chunks = self.embedder.generate_batch_embeddings(all_chunks)
            embedding_data = self.embedder.prepare_embedding_data(embedded_chunks)

            logger.info(f"Embedding items prepared: {len(embedding_data)}")

            if not embedding_data:
                logger.warning(
                    f"No embeddings generated for {source_file} (User: {self.user})"
                )
                return {"file_name": source_file, "status": "NO_EMBEDDINGS"}

            # 5️⃣ Prepare DB payload
            ids, embeddings, documents, metadatas = [], [], [], []

            for item in embedding_data:
                m = item["metadata"]
                ids.append(m["chunk_id"])
                embeddings.append(item["embedding_vector"])
                documents.append(item["text"])
                metadatas.append({
                    "source_file": source_file,
                    "page_number": m.get("page_number"),
                    "chunk_id": m.get("chunk_id"),
                    "user": self.user
                })

            logger.info(
                f"Storing {len(ids)} vectors into collection user_{self.user}"
            )

            # 6️⃣ Store in ChromaDB
            self.vector_db.add_documents(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            logger.info(
                f"Ingestion SUCCESS for {source_file} (User: {self.user})"
            )

            return {"file_name": source_file, "status": "SUCCESS"}

        except Exception as e:
            logger.exception(
                f"Failed to process {source_file} (User: {self.user})"
            )
            raise e

    def process_multiple_documents(self, pdf_paths: list):
        return [self.process_single_document(path) for path in pdf_paths]
