from backend.search_engine import SearchEngine
from backend.qa_engine import QAEngine

engine = SearchEngine()
qa = QAEngine()

history = []

questions = [
    "Explain OpenAI API setup",
    "What is the chunk overlap requirement?",
    "How many tasks are there in total?",
    "Compare ingestion pipeline vs similarity search",
    "What is the salary of the CEO of Google?"  # unanswerable intentionally
]

for q in questions:
    print("\n" + "=" * 90)
    print("QUESTION:", q)

    retrieved = engine.search_similar_chunks(q, k=5, threshold=0.7)

    result = qa.generate_answer(
        question=q,
        retrieved_chunks=retrieved,
        conversation_history=history
    )

    print("\nANSWER:\n", result["answer"])
    print("\nCITATIONS:", result["citations"])
    print("USED_CONTEXT:", result["used_context"])
    print("LATENCY:", result["latency_sec"], "sec")

    # save history for continuity
    history.append({"question": q, "answer": result["answer"]})
