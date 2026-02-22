from backend.pdf_processor import PDFProcessor

PDF_FILES = [
    "data/sample_pdfs/simple.pdf"
]

for pdf_path in PDF_FILES:
    print("\n" + "=" * 80)
    print(f"Processing: {pdf_path}")

    try:
        processor = PDFProcessor(pdf_path)

        metadata = processor.get_pdf_metadata()
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")

        print("\nExtracting text using PyMuPDF...")
        result = processor.extract_text_pymupdf()

        for page, text in result["text_by_page"].items():
            print(f"\n--- Page {page} ---")
            print(text[:500])  # print first 500 characters only

    except Exception as e:
        print(f"Error: {e}")
