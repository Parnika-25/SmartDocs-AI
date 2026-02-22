# import logging
# import os
# import re
# import time
# import shutil
# from functools import wraps

# # ==========================
# # Custom Exception Classes
# # ==========================

# class PDFProcessingError(Exception):
#     """Raised when PDF cannot be processed or is corrupted."""

# class EmbeddingError(Exception):
#     """Raised when embedding generation fails."""

# class DatabaseError(Exception):
#     """Raised when vector database operations fail."""

# class APIError(Exception):
#     """Raised for external API failures."""

# class ValidationError(Exception):
#     """Raised for invalid user input."""


# # ==========================
# # Logging Configuration
# # ==========================

# LOG_DIR = "logs"
# LOG_FILE = os.path.join(LOG_DIR, "app.log")

# os.makedirs(LOG_DIR, exist_ok=True)

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger("SmartDocsAI")


# # ==========================
# # Input Validation Helpers
# # ==========================

# MAX_FILE_SIZE_MB = 10
# MAX_QUERY_LENGTH = 500

# def validate_pdf(file):
#     if not file:
#         raise ValidationError("No file uploaded.")

#     if not file.name.lower().endswith(".pdf"):
#         raise ValidationError("Only PDF files are allowed.")

#     if file.size == 0:
#         raise ValidationError("Uploaded file is empty.")

#     if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
#         raise ValidationError("File size exceeds 10MB limit.")

# def validate_query(query: str):
#     if not query or not query.strip():
#         raise ValidationError("Query cannot be empty.")

#     if len(query) > MAX_QUERY_LENGTH:
#         raise ValidationError("Query exceeds 500 character limit.")

#     # Basic sanitization to avoid injection
#     if re.search(r"[<>;{}$]", query):
#         raise ValidationError("Query contains invalid characters.")

#     return query.strip()


# # ==========================
# # Retry Decorator (API Calls)
# # ==========================

# def retry_on_failure(retries=3, delay=5, allowed_exceptions=(APIError,)):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             for attempt in range(1, retries + 1):
#                 try:
#                     return func(*args, **kwargs)
#                 except allowed_exceptions as e:
#                     logger.warning(f"Retry {attempt}/{retries} after error: {e}")
#                     if attempt == retries:
#                         raise
#                     time.sleep(delay)
#         return wrapper
#     return decorator


# # ==========================
# # Health Check
# # ==========================

# def check_system_health(db=None, api_client=None):
#     health = {
#         "database": False,
#         "api": False,
#         "disk_space": False
#     }

#     # DB check
#     try:
#         if db:
#             db.get_collection_stats()
#         health["database"] = True
#     except Exception as e:
#         logger.error(f"Database health check failed: {e}")

#     # API check
#     try:
#         if api_client:
#             api_client.ping()
#         health["api"] = True
#     except Exception as e:
#         logger.error(f"API health check failed: {e}")

#     # Disk space check
#     try:
#         total, used, free = shutil.disk_usage(".")
#         health["disk_space"] = free > (500 * 1024 * 1024)  # 500MB
#     except Exception as e:
#         logger.error(f"Disk health check failed: {e}")

#     return health
import logging
import os
import re
import time
import shutil
from functools import wraps

# ==========================
# Custom Exception Classes
# ==========================

class PDFProcessingError(Exception):
    """Raised when PDF cannot be processed or is corrupted."""

class EmbeddingError(Exception):
    """Raised when embedding generation fails."""

class DatabaseError(Exception):
    """Raised when vector database operations fail."""

class APIError(Exception):
    """Raised for external API failures."""

class ValidationError(Exception):
    """Raised for invalid user input."""


# ==========================
# Logging Configuration
# ==========================

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SmartDocsAI")


# ==========================
# Input Validation Helpers
# ==========================

MAX_FILE_SIZE_MB = 10
MAX_QUERY_LENGTH = 500


def validate_pdf(file):
    """
    Validates uploaded PDF files.
    Works for BOTH:
    - Streamlit UploadedFile
    - FastAPI UploadFile
    """

    if not file:
        raise ValidationError("No file uploaded.")

    # ✅ Works for FastAPI (file.filename) & Streamlit (file.name)
    filename = getattr(file, "filename", None) or getattr(file, "name", None)

    if not filename:
        raise ValidationError("Invalid file object.")

    if not filename.lower().endswith(".pdf"):
        raise ValidationError("Only PDF files are allowed.")

    # -------- File size checks --------
    # Streamlit provides file.size
    if hasattr(file, "size"):
        if file.size == 0:
            raise ValidationError("Uploaded file is empty.")

        if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValidationError("File size exceeds 10MB limit.")

    return True


def validate_query(query: str):
    if not query or not query.strip():
        raise ValidationError("Query cannot be empty.")

    if len(query) > MAX_QUERY_LENGTH:
        raise ValidationError("Query exceeds 500 character limit.")

    # Basic sanitization to avoid injection-like input
    if re.search(r"[<>;{}$]", query):
        raise ValidationError("Query contains invalid characters.")

    return query.strip()


# ==========================
# Retry Decorator (API Calls)
# ==========================

def retry_on_failure(retries=3, delay=5, allowed_exceptions=(APIError,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    logger.warning(f"Retry {attempt}/{retries} after error: {e}")
                    if attempt == retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


# ==========================
# Health Check Utility
# ==========================

def check_system_health(db=None, api_client=None):
    """
    Returns system health status for:
    - Database
    - External API
    - Disk space
    """
    health = {
        "database": False,
        "api": False,
        "disk_space": False
    }

    # Database check
    try:
        if db:
            db.get_collection_stats()
        health["database"] = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    # API check (optional)
    try:
        if api_client and hasattr(api_client, "ping"):
            api_client.ping()
        health["api"] = True
    except Exception as e:
        logger.error(f"API health check failed: {e}")

    # Disk space check (minimum 500MB)
    try:
        total, used, free = shutil.disk_usage(".")
        health["disk_space"] = free > (500 * 1024 * 1024)
    except Exception as e:
        logger.error(f"Disk health check failed: {e}")

    return health