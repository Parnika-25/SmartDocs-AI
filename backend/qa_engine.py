# from typing import List, Dict
# from backend.openai_helper import OpenAIHelper
# from utils.error_handler import retry_on_failure, APIError

# class QAEngine:
#     def __init__(self):
#         self.client = OpenAIHelper()

#     def format_context(self, chunks):
#         """Formats retrieved chunks for the LLM prompt."""
#         return "\n\n".join(
#             f"[Source: {c['source_file']}, Page: {c['page_number']}]\n{c['chunk_text']}"
#             for c in chunks
#         )

#     def parse_citations(self, text):
#         """Extracts citations using regex to match the required format."""
#         return [
#             {"source_file": f, "page_number": int(p)}
#             for f, p in re.findall(r"\[Source:\s*(.*?),\s*Page:\s*(\d+)\]", text)
#         ]

#     @retry_on_failure(retries=3, delay=5)
#     def _call_llm(self, messages):
#         return self.client.get_completion(messages, timeout=30)

#     def generate_answer(self, question, retrieved_chunks, conversation_history=None):
#         if not retrieved_chunks:
#             return {"answer": "Answer not found in documents.", "citations": []}

#         context = self.format_context(retrieved_chunks)

#         # Updated system prompt to ensure citations are parseable
#         messages = [{
#             "role": "system",
#             "content": (
#                 "You are an expert assistant. Answer ONLY using the provided context. "
#                 "At the end of your response, you MUST cite your sources using this exact format: "
#                 "[Source: filename.pdf, Page: X]. Do not deviate from this format."
#             )
#         }]

#         if conversation_history:
#             for h in conversation_history[-3:]:
#                 messages.append({"role": "user", "content": h["question"]})
#                 messages.append({"role": "assistant", "content": h["answer"]})

#         messages.append({"role": "user", "content": f"Context:\n{context}\n\nQ: {question}"})

#         try:
#             text = self._call_llm(messages)
#             citations = self.parse_citations(text)
#             return {"answer": text, "citations": citations}
#         except APIError:
#             return {"answer": "AI service unavailable.", "citations": []}
import re  # Added missing import to fix NameError
import logging
from typing import List, Dict
from backend.openai_helper import OpenAIHelper
from utils.error_handler import retry_on_failure, APIError

# Setup logger for Task 15 centralized logging
logger = logging.getLogger(__name__)

class QAEngine:
    def __init__(self):
        """Initializes the LLM client."""
        self.client = OpenAIHelper()

    def format_context(self, chunks: List[Dict]) -> str:
        """Formats retrieved chunks for the LLM prompt."""
        return "\n\n".join(
            f"[Source: {c['source_file']}, Page: {c['page_number']}]\n{c['chunk_text']}"
            for c in chunks
        )

    def parse_citations(self, text: str) -> List[Dict]:
        """Extracts citations using regex to match the required format [Source: ..., Page: ...]."""
        # This requires the 'import re' added at the top
        return [
            {"source_file": f, "page_number": int(p)}
            for f, p in re.findall(r"\[Source:\s*(.*?),\s*Page:\s*(\d+)\]", text)
        ]

    @retry_on_failure(retries=3, delay=5)
    def _call_llm(self, messages: List[Dict]) -> str:
        """Calls the LLM with automatic retry logic and 30s timeout (Task 15)."""
        return self.client.get_completion(messages, timeout=30)

    def generate_answer(self, question: str, retrieved_chunks: List[Dict], conversation_history: List[Dict] = None) -> Dict:
        """
        Generates an answer based on retrieved context with citation parsing.
        Includes graceful degradation and error handling (Task 15).
        """
        if not retrieved_chunks:
            logger.warning(f"No chunks retrieved for question: {question}")
            return {"answer": "Answer not found in documents.", "citations": []}

        context = self.format_context(retrieved_chunks)

        # System prompt ensures the LLM uses a parseable citation format
        messages = [{
            "role": "system",
            "content": (
                "You are an expert assistant. Answer ONLY using the provided context. "
                "At the end of your response, you MUST cite your sources using this exact format: "
                "[Source: filename.pdf, Page: X]. Do not deviate from this format."
            )
        }]

        # Include last 3 exchanges for context-aware Q&A
        if conversation_history:
            for h in conversation_history[-3:]:
                messages.append({"role": "user", "content": h["question"]})
                messages.append({"role": "assistant", "content": h["answer"]})

        messages.append({"role": "user", "content": f"Context:\n{context}\n\nQ: {question}"})

        try:
            # LLM Call with Task 15 retry and timeout constraints
            text = self._call_llm(messages)
            citations = self.parse_citations(text)
            return {"answer": text, "citations": citations}
        
        except APIError as ae:
            # Task 15: Graceful error handling for API failures
            logger.error(f"API Error in QAEngine: {ae}")
            return {"answer": "AI service unavailable. Please check your connection or API credits.", "citations": []}
        
        except Exception as e:
            # Catch-all for unexpected issues to prevent app crash
            logger.error(f"Unexpected error in QAEngine: {e}")
            return {"answer": "An unexpected error occurred while generating the answer.", "citations": []}