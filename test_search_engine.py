from backend.search_engine import SearchEngine

queries = [
    "What is Task 1 about?",
    "Explain OpenAI API setup",
    "What is the chunk overlap requirement?",
    "How many tasks are there in total?",
    "What does the ingestion pipeline do?",
    "What is ChromaDB used for?",
    "How does similarity search work?",
    "Explain token-based chunking",
    "What is the file size limit for upload?",
    "What is the role of embeddings?"
]

engine = SearchEngine()

for q in queries:
    print("\n" + "=" * 80)
    print("Query:", q)

    results = engine.search_similar_chunks(q, k=5, threshold=0.7)

    if not results:
        print("❌ No relevant results found (below threshold)")
        continue

    for r in results:
        print("\n✅ Match")
        print("Score:", r["relevance_score"])
        print("File:", r["source_file"])
        print("Page:", r["page_number"])
        print("Chunk Index:", r["chunk_index"])
        print("Text Preview:", r["chunk_text"][:200])
