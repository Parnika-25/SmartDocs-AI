# 📘 SmartDocs AI – Intelligent Multi-Document Q&A System

A full-stack Retrieval-Augmented Generation (RAG) application that enables users to upload multiple PDF documents and ask intelligent, context-aware questions with source attribution.

## ✨ Features

- **Multi-PDF Upload** - Handle multiple documents simultaneously
- **Intelligent Q&A** - Ask questions and get answers grounded in document content
- **Smart Text Processing** - PDF extraction and preprocessing with PyMuPDF and pdfplumber
- **Semantic Search** - Token-based chunking with cosine similarity matching
- **Advanced Embeddings** - 1536-dimensional OpenAI embeddings for semantic understanding
- **Persistent Storage** - ChromaDB for reliable vector database storage
- **Source Attribution** - Know exactly which documents your answers come from
- **Session Management** - Track and export Q&A history
- **Comprehensive Testing** - Unit and integration tests with pytest

## 🏗️ Architecture
```
┌─────────────────────────────────────┐
│         React Frontend              │
│       (smartdocs-frontend)          │
└─────────────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────┐
│           FastAPI Backend           │
│            (Python 3.8+)            │
└─────────────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────┐
│      PDF Processing Pipeline        │
├─────────────────────────────────────┤
│  • Text Extraction (PyMuPDF)        │
│  • Text Cleaning & Normalization    │
│  • Tokenization (tiktoken)          │
│  • Overlapping Chunking             │
└─────────────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────┐
│        OpenAI Embeddings API        │
│     (text-embedding-ada-002)        │
│        1536-Dimensional Vectors     │
└─────────────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────┐
│             ChromaDB                │
│        (Persistent Vector DB)       │
└─────────────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────┐
│      Similarity Search Engine       │
│        (Cosine Similarity)          │
├─────────────────────────────────────┤
│  • Top-K Retrieval                  │
│  • Threshold Filtering              │
│  • Context Window Expansion         │
└─────────────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────┐
│   Context-Aware Response Generator  │
│              (GPT-4)                │
│  • Prompt Engineering               │
│  • Citation Extraction              │
│  • Source Attribution               │
└─────────────────────────────────────┘
```
## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern Python web framework
- **OpenAI API** - Embeddings and LLM
- **ChromaDB** - Vector database
- **PyMuPDF** - PDF text extraction
- **pdfplumber** - Advanced PDF parsing
- **tiktoken** - Token counting
- **pytest** - Testing framework
- **python-dotenv** - Environment management

### Frontend
- **React 18+** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **JavaScript (ES6+)**

## 📁 Project Structure
```
Pdf-ai-app/
│
├── backend/                     # Python FastAPI backend
│   ├── main.py
│   ├── pdf_processor.py
│   ├── text_cleaner.py
│   ├── text_chunker.py
│   ├── embeddings.py
│   ├── vector_db.py
│   ├── ingestion_pipeline.py
│   ├── search_engine.py
│   ├── qa_engine.py
│   ├── session_manager.py
│   └── batch_processor.py
│
├── smartdocs-frontend/          # React frontend application
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── api/
│   ├── package.json
│   └── vite.config.js
│
├── utils/                       # Shared utility modules
│   └── error_handler.py
│
├── data/                        # ChromaDB storage & sample data
│   └── chroma_db/
│
├── uploads/                     # Uploaded PDF storage
│
├── tests/                       # Unit & integration tests
│   ├── test_pdf_processor.py
│   ├── test_text_cleaner.py
│   ├── test_chunker.py
│   ├── test_embeddings.py
│   ├── test_vector_db.py
│   ├── test_search_engine.py
│   └── test_integration.py
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── README.md                    # Project overview
├── USER_GUIDE.md                # End-user documentation
├── DEVELOPER_GUIDE.md           # Developer documentation
└── DEPLOYMENT.md                # Deployment instructions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup


# Navigate to root directory
```bash
cd Pdf-ai-app
```
# Create virtual environment
```bash
python -m venv venv
```
# Activate virtual environment
# On Windows:
```
venv\Scripts\activate
```
# On macOS/Linux:
```
source venv/bin/activate
```
# Install dependencies
```
pip install -r requirements.txt
```
Configure environment variables:
# Create .env file
```
echo OPENAI_API_KEY=your_api_key_here > .env
```
Run the backend:

```bash
uvicorn backend.main:app --reload
Backend API available at: http://localhost:8000
```
Frontend Setup
```bash
# Navigate to frontend directory
cd smartdocs-frontend
```
# Install dependencies
```
npm install
```
# Set environment variable
```
echo VITE_API_BASE_URL=http://localhost:8000 > .env.local
```
# Start development server
```
npm run dev
Frontend available at: http://localhost:5173
```
🧪 Testing
Run the test suite to verify all components:

```bash
# Run all tests
pytest
```
# Run specific test file
```
pytest test_embeddings.py -v
```
# Run with coverage
```
pytest --cov=backend tests/
```
Available tests:

test_embeddings.py - OpenAI embedding functionality
test_extraction.py - PDF text extraction
test_text_chunking.py - Text chunking logic
test_text_cleaning.py - Text preprocessing
test_vector_db.py - ChromaDB operations
test_search_engine.py - Similarity search
test_qa_engine.py - Q&A generation
test_ingestion_pipeline.py - Full pipeline
test_openai_connection.py - API connectivity
## 📖 Documentation

The project includes comprehensive documentation for both end users and developers:

- **USER_GUIDE.md** – Step-by-step guide on how to use the application.
- **DEVELOPER_GUIDE.md** – Detailed explanation of system architecture, modules, API design, and extension points.

Please refer to these documents for deeper insights into usage and implementation.

---

## 🔧 API Endpoints

The FastAPI backend exposes the following core endpoints:

### 📤 Document Management

- `POST /upload`  
  Upload one or more PDF documents for processing and indexing.

---

### ❓ Query Processing

- `POST /query`  
  Submit a user question and receive a context-aware response generated from indexed documents.

---

### 🕘 Session Management

- `GET /history`  
  Retrieve complete Q&A session history.

- `DELETE /clear`  
  Clear current session data and reset conversation state.

For detailed request/response schemas and implementation details, see **DEVELOPER_GUIDE.md**.

---

## 🌟 Key Implementation Details

### 📄 Text Processing Pipeline

1. **Extraction**  
   PyMuPDF extracts raw text from uploaded PDFs.  
   pdfplumber is used as a fallback for complex layouts.

2. **Cleaning**  
   - Normalize whitespace  
   - Remove special characters  
   - Standardize encoding  

3. **Chunking**  
   - Token-based chunking (1000 tokens)  
   - 200-token overlap  
   - Metadata tracking (file name, page number, chunk ID)

4. **Embedding**  
   - Each chunk converted into a 1536-dimensional vector  
   - Uses OpenAI `text-embedding-ada-002` model  

5. **Storage**  
   - Embeddings stored in ChromaDB  
   - Metadata preserved for citation and traceability  

---

### 🔍 Query Processing Workflow

1. **Vectorization**  
   User query converted into embedding.

2. **Similarity Search**  
   - Cosine similarity used for matching  
   - Top-k results retrieved  
   - Threshold filtering removes low-relevance matches  

3. **Context Construction**  
   Relevant chunks compiled into structured prompt.

4. **Response Generation**  
   GPT-4 generates answer strictly based on provided context.

---

### 📌 Source Attribution

Every response includes:

- Exact source document names
- Page references (when available)
- Relevant context snippets
- Confidence/relevance scores

This ensures transparency and minimizes hallucination.

---

## 🔐 Security & Best Practices

- API keys stored securely in `.env` (never committed to version control).
- Environment variables used for sensitive configurations.
- Strict PDF file validation (type and size checks).
- Input sanitization for user queries.
- Rate limiting recommended for production deployment.
- HTTPS required for secure API communication.
- CORS properly configured for frontend-backend interaction.

---

## 🤝 Contributing

Contributions are welcome.

1. Create a feature branch:

```
git checkout -b feature/your-feature-name
```

2. Commit your changes:
```
git commit -m "Add meaningful feature description"
```

3. Push to your branch:

```
git push origin feature/your-feature-name
```

4. Open a Pull Request.

Please ensure all tests pass before submitting changes.

---

## 👤 Author

**Keerthi Mittapalli**  
AI & Machine Learning Developer  
SmartDocs AI Internship Project

---

## 💬 Support

For questions, issues, or feature requests:

- Open a GitHub Issue  
- Refer to USER_GUIDE.md or DEVELOPER_GUIDE.md  
- Review logs for debugging information  

Thank you for using SmartDocs AI 🚀
