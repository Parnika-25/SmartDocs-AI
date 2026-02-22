# import os
# import openai
# from dotenv import load_dotenv

# from utils.error_handler import APIError, logger

# load_dotenv()


# class OpenAIHelper:
#     def __init__(self):
#         api_key = os.getenv("OPENAI_API_KEY")
#         if not api_key:
#             raise APIError("OpenAI API key not configured")

#         openai.api_key = api_key

#     def get_completion(
#         self,
#         messages,
#         model="gpt-3.5-turbo",
#         temperature=0.2,
#         timeout=30
#     ):
#         """
#         messages: list of dicts
#         [
#           {"role": "system", "content": "..."},
#           {"role": "user", "content": "..."}
#         ]
#         """
#         try:
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=messages,
#                 temperature=temperature,
#                 request_timeout=timeout   # ✅ correct param for legacy SDK
#             )

#             return response["choices"][0]["message"]["content"]

#         # -------- OpenAI-specific errors --------
#         except openai.error.RateLimitError:
#             logger.warning("OpenAI rate limit exceeded")
#             raise APIError("Rate limit exceeded. Please try again later.")

#         except openai.error.AuthenticationError:
#             logger.error("Invalid OpenAI API key")
#             raise APIError("Invalid OpenAI API key.")

#         except openai.error.InsufficientQuotaError:
#             logger.error("OpenAI quota exhausted")
#             raise APIError("Insufficient OpenAI credits.")

#         except openai.error.Timeout:
#             logger.error("OpenAI request timed out")
#             raise APIError("OpenAI request timed out.")

#         # -------- Generic fallback --------
#         except Exception as e:
#             logger.error(f"OpenAI API error: {e}")
#             raise APIError("OpenAI service error.")
import os
import openai
from dotenv import load_dotenv

from utils.error_handler import APIError, logger

load_dotenv()


class OpenAIHelper:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise APIError("OpenAI API key not configured")

        openai.api_key = api_key

    def get_completion(
        self,
        messages,
        model="gpt-3.5-turbo",
        temperature=0.2,
        timeout=30
    ):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                request_timeout=timeout
            )

            return response["choices"][0]["message"]["content"]

        # -------- OpenAI-specific errors --------
        except openai.error.RateLimitError as e:
            logger.error(f"OpenAI rate/quota error: {e}")
            raise APIError(
                "OpenAI quota or rate limit exceeded. Please check your plan."
            )

        except openai.error.AuthenticationError:
            logger.error("Invalid OpenAI API key")
            raise APIError("Invalid OpenAI API key.")

        except openai.error.Timeout:
            logger.error("OpenAI request timed out")
            raise APIError("OpenAI request timed out.")

        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI SDK error: {e}")
            raise APIError("OpenAI service error.")

        # -------- Final fallback --------
        except Exception as e:
            logger.exception("Unexpected OpenAI error")
            raise APIError("Unexpected OpenAI service error.")
