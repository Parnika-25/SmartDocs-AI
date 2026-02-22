from backend.ingestion_pipeline import DocumentIngestion
from backend.vector_db import VectorDatabase
import time

PDF_FILES = [
    "data/sample_pdfs/simple.pdf"
]

pipeline = DocumentIngestion()

print("\n🚀 Starting ingestion pipeline for 1 PDF...\n")

results = pipeline.process_multiple_documents(PDF_FILES)

print("\n✅ Pipeline Results:")
for res in results:
    print(res)

print("\n📊 Live Status:")
print(pipeline.get_processing_status())

# Verify storage
db = VectorDatabase()
stats = db.get_collection_stats()

print("\n📌 ChromaDB Collection Stats After Ingestion:")
print(stats)

print("\n✅ Integration test completed!")
