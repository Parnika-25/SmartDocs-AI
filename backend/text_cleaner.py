import re
import unicodedata


class TextCleaner:
    """
    TextCleaner handles preprocessing and cleaning of extracted PDF text.
    Each method performs a specific cleaning task and returns cleaned text.
    """

    def __init__(self):
        pass

    def remove_extra_whitespace(self, text: str) -> str:
        """
        Normalize excessive spaces, tabs, and line breaks.
        - Converts multiple spaces to single space
        - Reduces multiple newlines
        """
        if not text or not text.strip():
            return ""

        # Replace tabs with space
        text = text.replace("\t", " ")

        # Collapse multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Collapse multiple newlines
        text = re.sub(r"\n{2,}", "\n", text)

        return text.strip()

    def remove_special_characters(self, text: str) -> str:
        """
        Remove unwanted special characters while keeping
        letters, numbers, and common punctuation.
        """
        if not text or not text.strip():
            return ""

        # Keep letters, numbers, punctuation, and whitespace
        text = re.sub(r"[^a-zA-Z0-9.,!?;:'\"()\-\n ]", "", text)

        return text.strip()

    def remove_headers_footers(self, text: str) -> str:
        """
        Remove common headers, footers, and page numbers.
        Handles:
        - Page numbers like 'Page 1', '1', '--- Page 1 ---'
        - Repeated decorative lines
        """
        if not text or not text.strip():
            return ""

        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            stripped = line.strip()

            # Skip page numbers
            if re.fullmatch(r"(page\s*)?\d+", stripped.lower()):
                continue

            # Skip decorative separators
            if re.fullmatch(r"[-_=#]{3,}", stripped):
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()

    def normalize_text(self, text: str) -> str:
        """
        Normalize text encoding and casing.
        - Unicode normalization (NFKD)
        - Convert text to lowercase
        """
        if not text or not text.strip():
            return ""

        # Normalize unicode characters
        text = unicodedata.normalize("NFKD", text)

        # Convert to lowercase
        text = text.lower()

        return text.strip()

    def clean_text(self, text: str) -> str:
        """
        Master cleaning function.
        Applies all preprocessing steps in sequence.
        """
        if not text or not text.strip():
            return ""

        text = self.remove_extra_whitespace(text)
        text = self.remove_special_characters(text)
        text = self.remove_headers_footers(text)
        text = self.normalize_text(text)

        return text
