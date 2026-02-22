# 📖 USER GUIDE – SmartDocs AI

Welcome to SmartDocs AI – an intelligent multi-document Q&A system powered by Retrieval-Augmented Generation (RAG).

This guide explains how to use the application effectively.

---

## 🚀 Getting Started

1. Open the deployed application URL.
2. Ensure backend API is running.
3. Upload one or more PDF documents.
4. Start asking questions!

---

## 📂 Uploading Documents

1. Navigate to the Upload section.
2. Click "Upload PDFs".
3. Select one or more PDF files (max 10MB per file).
4. Click "Process Documents".
5. Wait for the processing indicator to complete.

What happens in the background:
- PDFs are extracted
- Text is cleaned
- Content is chunked
- Embeddings are generated
- Stored in ChromaDB

---

## ❓ Asking Questions

1. Go to the Q&A section.
2. Enter your question in the input field.
3. Click "Ask" or press Enter.
4. View generated answer with citations.

---

## 📌 Understanding Answers

Each response includes:

- Generated answer (based strictly on document context)
- Source document names
- Page numbers (when available)
- Relevance scores
- Context snippets
- Document contribution visualization (if enabled)


This ensures transparency and prevents hallucination.

---

## 📊 Semantic Search

Behind the scenes:

- Your query is converted into an embedding.
- The system retrieves top-k relevant chunks.
- Low similarity results are filtered out.
- Context is passed to GPT-4 for final answer generation.

---

## 💾 Session Management

You can:

- View full chat history
- Clear session
- Export conversation
- Track previous Q&A interactions

---

## 📤 Exporting Chat History

Export options include:

- TXT file
- Markdown file
- PDF file

Exports include:
- Questions
- Answers
- Source citations
- Timestamps

---

## ⚠️ Best Practices

For best results:

- Ask clear, specific questions.
- Upload related documents together.
- Avoid vague queries like “Explain everything.”
- Ensure PDFs contain extractable text (not scanned images only).

---

## 🔐 Data Privacy

- Documents are processed locally on your backend.
- API keys are stored securely in environment variables.
- Uploaded files are stored in `/uploads` directory.
- No data is shared externally except embeddings & GPT requests.

---

## 🆘 Troubleshooting

Problem: No answer returned  
→ Ensure documents were processed successfully.

Problem: API error  
→ Verify OPENAI_API_KEY is valid.

Problem: Slow response  
→ Large PDFs may take longer for ingestion.

---

## 📞 Support

For issues:
- Check logs
- Review README.md
- Refer to DEVELOPER_GUIDE.md
- Open GitHub issue

Example citation:

