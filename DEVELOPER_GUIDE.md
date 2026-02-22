# 🧠 DEVELOPER GUIDE – SmartDocs AI

This guide explains system architecture, modules, and extension points.

---

# 🏗️ System Architecture
```
Frontend (React)
        ↓
FastAPI Backend
        ↓
PDF Processing Pipeline
        ↓
Embedding Generation
        ↓
ChromaDB (Vector Store)
        ↓
Similarity Search
        ↓
GPT-4 Response Generation
```
---

# 📁 Backend Modules

## main.py
Entry point for FastAPI.
Defines API endpoints and CORS configuration.

---

## pdf_processor.py

Responsibilities:
- Extract text from PDFs using PyMuPDF
- Fallback to pdfplumber
- Extract metadata (pages, title, author)
- Handle corrupted or password-protected files

---

## text_cleaner.py

Functions:
- remove_extra_whitespace()
- remove_special_characters()
- normalize_text()
- remove_headers_footers()
- clean_text()

Purpose:
Normalize text before chunking.

---

## text_chunker.py

Features:
- Token-based chunking (1000 tokens)
- 200 token overlap
- Sentence-aware splitting
- Metadata tracking (chunk_id, page_number)

Why overlap?
Maintains semantic continuity between chunks.

---

## embeddings.py

Responsibilities:
- Generate OpenAI embeddings
- 1536-dimensional vector verification
- Retry logic with exponential backoff
- Rate limiting
- Batch embedding support

Model used:
text-embedding-ada-002

---

## vector_db.py

Handles:
- ChromaDB initialization
- Collection creation
- Add/update/delete documents
- Persistent storage
- Collection statistics

---

## ingestion_pipeline.py

Orchestrates:

PDF → Clean → Chunk → Embed → Store

Includes:
- Progress tracking
- Logging
- Error rollback

---

## search_engine.py

Implements:
- Query embedding
- Cosine similarity search
- Top-k retrieval
- Threshold filtering (default 0.7)
- Context window expansion

---

## qa_engine.py

Core logic:

1. Receive user question
2. Inject retrieved context
3. Build structured prompt
4. Call GPT-4
5. Extract citations
6. Return grounded response

Includes:
- Token management
- Conversation memory
- Citation parsing

---

# 📡 API Endpoints

POST /upload  
Upload PDF documents.

POST /query  
Submit user question.

GET /history  
Retrieve session Q&A history.

DELETE /clear  
Clear session data.

---

# 🧪 Testing Strategy

Located in `/tests`:

Unit Tests:
- test_pdf_processor.py
- test_text_cleaner.py
- test_chunker.py
- test_embeddings.py
- test_vector_db.py
- test_search_engine.py

Integration Test:
- test_integration.py


---

# ⚡ Performance Optimizations

- Caching expensive operations
- Batch embedding generation
- Persistent vector storage
- Context window optimization
- Lazy loading in frontend

---

# 🔐 Security Considerations

- API key stored in `.env`
- CORS configured
- File type validation (.pdf only)
- File size validation (10MB limit)
- Error handling with custom exceptions

---

# 🔧 Extending the System

To change embedding model:
Modify `embeddings.py`

To change chunk size:
Modify `text_chunker.py`

To switch to GPT-4o:
Update model name in `qa_engine.py`

To add hybrid search:
Combine keyword + vector similarity in `search_engine.py`

---

# 🚀 Production Deployment

Backend → Render  
Frontend → Vercel  

Ensure:
- Environment variables set
- CORS configured
- Persistent storage enabled

---

# 👤 Maintainer

Keerthi Mittapalli  
AI & ML Developer


