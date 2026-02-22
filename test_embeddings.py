import time
import json
from backend.text_chunker import TextChunker
from backend.embeddings import EmbeddingGenerator

# Create 10 sample chunks
sample_text = "This is a test chunk for embedding generation. " * 30

chunker = TextChunker()
chunks = chunker.create_chunks(
    text=sample_text,
    source_file="sample.pdf",
    page_number=1,
    strategy="sentences"
)

# Take first 10 chunks
chunks = chunks[:10]

generator = EmbeddingGenerator()

start_time = time.time()

print("Generating embeddings for 10 chunks...")

embedded_chunks = generator.generate_batch_embeddings(chunks)
final_data = generator.prepare_embedding_data(embedded_chunks)

end_time = time.time()
total_time = end_time - start_time

# Verify dimensions
for i, item in enumerate(final_data):
    emb = item["embedding_vector"]
    if len(emb) != 1536:
        raise Exception(f"Chunk {i} embedding dimension incorrect: {len(emb)}")

print("✅ All embeddings are 1536-dimensional")

# Save embeddings to JSON
output_file = "data/sample_embeddings.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2)

print(f"✅ Saved embeddings to: {output_file}")
print(f"⏱ Processing time: {total_time:.2f} seconds")
