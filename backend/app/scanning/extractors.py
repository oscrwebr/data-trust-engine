from app.scanning.detectors import re
from app.scanning.regex_patterns import re
import pymupdf


# Extract text from PDF into dict
def extract_text_from_pdf(file_bytes: bytes) -> dict:
    file = pymupdf.open(stream=file_bytes, filetype="pdf")
    extracted_text = {}

    # Make page numbers 1 indexed, because user think in page 1, 2, 3 not 0, 1, 2
    for page_number in range(len(file)):
        page = file.load_page(page_number)
        text = page.get_text("text")

        # Normalisation to remove line breaks
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()

        extracted_text[page_number + 1] = text

    file.close()
    return extracted_text