# import concurrent.futures
# from backend.ingestion_pipeline import DocumentIngestion
# from utils.error_handler import logger

# class BatchProcessor:
#     def __init__(self, max_workers=3):
#         self.max_workers = max_workers
#         self.ingestor = DocumentIngestion()

#     def process_files_parallel(self, file_paths, progress_callback=None):
#         """Processes multiple files in parallel (Task 16)."""
#         results = []
#         # Use ThreadPoolExecutor for concurrent ingestion
#         with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
#             future_to_file = {executor.submit(self.ingestor.process_single_document, path): path for path in file_paths}
            
#             completed = 0
#             for future in concurrent.futures.as_completed(future_to_file):
#                 file_path = future_to_file[future]
#                 try:
#                     data = future.result()
#                     results.append(data)
#                 except Exception as e:
#                     logger.error(f"Error processing {file_path}: {e}")
                
#                 completed += 1
#                 if progress_callback:
#                     # Update UI progress bar
#                     progress_callback(completed / len(file_paths))
#         return results


import concurrent.futures
from backend.ingestion_pipeline import DocumentIngestion
from utils.error_handler import logger

class BatchProcessor:
    # ✅ Added 'user' to the constructor
    def __init__(self, user: str, max_workers=3):
        self.user = user
        self.max_workers = max_workers
        # ✅ Pass the user to the ingestor so data is stored in the correct collection/folder
        self.ingestor = DocumentIngestion(user=user)

    def process_files_parallel(self, file_paths, progress_callback=None):
        """Processes multiple files in parallel (Task 16)."""
        results = []
        # Use ThreadPoolExecutor for concurrent ingestion
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self.ingestor.process_single_document, path): path for path in file_paths}
            
            completed = 0
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    # This will now show up in your logs if a specific PDF fails
                    logger.error(f"Error processing {file_path}: {e}")
                
                completed += 1
                if progress_callback:
                    # Update UI progress bar
                    progress_callback(completed / len(file_paths))
        return results