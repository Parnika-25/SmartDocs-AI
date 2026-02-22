import time
from backend.vector_db import VectorDatabase
from backend.embeddings import EmbeddingGenerator


def run_test():
    print("\n✅ Initializing Vector DB...")
    db = VectorDatabase()
    db.verify_connection()
    print("✅ Connection Verified!")

    print("\n✅ Creating / Loading Collection...")
    db.create_collection()

    # Generate 5 sample embeddings
    generator = EmbeddingGenerator()

    sample_chunks = []
    for i in range(5):
        sample_chunks.append({
            "chunk_id": f"chunk_{i}",
            "chunk_index": i,
            "text": f"This is a sample chunk number {i}. It is used for testing ChromaDB persistence.",
            "source_file": "test.pdf",
            "page_number": i + 1,
            "token_count": 20,
            "word_count": 15,
            "char_count": 80
        })

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    print("\n✅ Generating embeddings and inserting into ChromaDB...")

    for chunk in sample_chunks:
        emb = generator.generate_embedding(chunk["text"])

        ids.append(chunk["chunk_id"])
        embeddings.append(emb)
        documents.append(chunk["text"])
        metadatas.append({
            "source_file": chunk["source_file"],
            "page_number": chunk["page_number"],
            "chunk_id": chunk["chunk_id"]
        })

    db.add_documents(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    print("✅ Inserted 5 embeddings successfully!")

    # Show stats
    stats = db.get_collection_stats()
    print("\n📊 Collection Stats:")
    print(stats)

    # Retrieve documents
    results = db.get_all_documents(limit=5)
    print("\n📌 Retrieved Documents:")
    for doc, meta in zip(results["documents"], results["metadatas"]):
        print("Text:", doc[:60], "...")
        print("Metadata:", meta)

    print("\n✅ Restart test for persistence...")
    time.sleep(2)

    # Restart DB object (simulate app restart)
    db2 = VectorDatabase()
    stats2 = db2.get_collection_stats()

    print("\n📊 Stats after restart:")
    print(stats2)

    if stats2["total_documents"] >= 5:
        print("\n✅ Persistence Verified: Data still exists after restart!")
    else:
        print("\n❌ Persistence Failed: Data missing after restart!")


if __name__ == "__main__":
    run_test()
