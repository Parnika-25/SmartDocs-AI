import fitz  # PyMuPDF
import pdfplumber
import os


class PDFProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

    def get_pdf_metadata(self):
        """
        Extract metadata: file name, total pages, title, author
        """
        try:
            doc = fitz.open(self.file_path)

            if doc.needs_pass:
                raise RuntimeError("Password-protected PDF")

            page_count = doc.page_count
            metadata = doc.metadata

            result = {
                "file_name": self.file_name,
                "total_pages": page_count,
                "title": metadata.get("title"),
                "author": metadata.get("author")
            }

            doc.close()
            return result

        except Exception as e:
            raise RuntimeError(f"Metadata extraction failed: {str(e)}")

    def extract_text_pymupdf(self):
        """
        Primary extraction method using PyMuPDF
        """
        try:
            text_by_page = {}

            doc = fitz.open(self.file_path)

            if doc.needs_pass:
                raise RuntimeError("Password-protected PDF")

            page_count = doc.page_count

            if page_count == 0:
                raise ValueError("Empty PDF document")

            for page_num in range(page_count):
                page = doc.load_page(page_num)
                text = page.get_text().strip()
                text_by_page[page_num + 1] = text

            doc.close()

            return {
                "file_name": self.file_name,
                "total_pages": page_count,
                "text_by_page": text_by_page
            }

        except fitz.FileDataError:
            raise RuntimeError("Corrupted or invalid PDF file")

        except Exception as e:
            raise RuntimeError(f"PyMuPDF extraction failed: {str(e)}")

    def extract_text_pdfplumber(self):
        """
        Fallback extraction method using pdfplumber
        """
        try:
            text_by_page = {}

            with pdfplumber.open(self.file_path) as pdf:
                page_count = len(pdf.pages)

                if page_count == 0:
                    raise ValueError("Empty PDF document")

                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    text_by_page[i + 1] = text.strip() if text else ""

            return {
                "file_name": self.file_name,
                "total_pages": page_count,
                "text_by_page": text_by_page
            }

        except Exception as e:
            raise RuntimeError(f"pdfplumber extraction failed: {str(e)}")
