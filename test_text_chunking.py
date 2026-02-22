from backend.text_chunker import TextChunker

sample_text_short = "This is a short document. It has only a few sentences."

sample_text_medium = " ".join(
    ["This is a medium-sized document sentence."] * 300
)

sample_text_long = " ".join(
    ["This is a long document sentence designed for stress testing."] * 1500
)

chunker = TextChunker()

tests = [
    ("short.pdf", 1, sample_text_short),
    ("medium.pdf", 5, sample_text_medium),
    ("long.pdf", 20, sample_text_long)
]

for file, page, text in tests:
    print("\n" + "=" * 80)
    print(f"Testing: {file}")

    chunks = chunker.create_chunks(
        text=text,
        source_file=file,
        page_number=page,
        strategy="sentences"
    )

    print(f"Total Chunks: {len(chunks)}")

    for chunk in chunks[:2]:
        print("\nChunk ID:", chunk["chunk_id"])
        print("Chunk Index:", chunk["chunk_index"])
        print("Tokens:", chunk["token_count"])
        print("Words:", chunk["word_count"])
        print("Preview:", chunk["text"][:200])
