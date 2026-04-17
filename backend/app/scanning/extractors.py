from app.scanning.detectors import re
from app.scanning.regex_patterns import re
import pymupdf


# Helper method for normalising text by deleting line breaks
def normalise_text(text: str):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()


# Extract text from .pdf filebytes into dict
def extract_text_from_pdf(file_bytes: bytes) -> dict:
    file = pymupdf.open(stream=file_bytes, filetype="pdf")
    extracted_text = {}

    # Make page numbers 1 indexed, because user think in page 1, 2, 3 not 0, 1, 2
    for page_number in range(len(file)):
        page = file.load_page(page_number)
        text = normalise_text(page.get_text("text"))

        extracted_text[page_number + 1] = text

    file.close()
    return extracted_text


# Extract text from .txt filebytes
def extract_text_from_txt(file_bytes: bytes) -> dict:
    text = file_bytes.decode("utf-8", errors="ignore")

    # Only one page on a .txt document therefore return as just page number 1
    return {
        1: normalise_text(text)
    }