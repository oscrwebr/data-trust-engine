from pathlib import Path

from app.scanning.extractors import *

FIXTURES_DIRECTORY = Path(__file__).resolve().parent / "fixtures"

# Helper method that reads a test file into bytes by using its path from the fixtures folder
def read_file_bytes(file_name: str):
    file_path = FIXTURES_DIRECTORY / file_name

    with open(file_path, "rb") as file:
        return file.read()


def test_extract_text_from_pdf_operational_report_document():
    # Read file bytes and extract text using PDF extractor
    file_bytes = read_file_bytes("operational_report_document.pdf")
    extracted_text = extract_text_from_pdf(file_bytes=file_bytes)
    
    # Assert all pages extracted
    assert len(extracted_text) == 4

    # Assert page number 1 (first) and number 4 (last) are extracted
    assert 1 in extracted_text
    assert 4 in extracted_text

    # Assert that some key words exist on the correct pages of the extracted text
    assert "Operational Performance Report" in extracted_text[1]
    assert "internal documentation section" in extracted_text[2]
    assert "14 King Street, Leeds" in extracted_text[3]
    assert "emma.thompson@northbridge-consulting.co.uk" in extracted_text[4]


def test_extract_text_from_pdf_realistic_contract_document():
    # Read file bytes and extract text using PDF extractor
    file_bytes = read_file_bytes("realistic_contract_document.pdf")
    extracted_text = extract_text_from_pdf(file_bytes=file_bytes)

    # Assert all pages extracted
    assert len(extracted_text) == 5

    # Assert page number 1 (first) and number 5 (last) are extracted
    assert 1 in extracted_text
    assert 5 in extracted_text

    # Assert that some key words exist on the correct pages of the extracted text
    assert "Liam Davies" in extracted_text[1]
    assert "5919 9391 1212" in extracted_text[2]
    assert "WEST 8165 5322 4604 6004" in extracted_text[3]
    assert "agreement should be addressed to the company offices located at 18 Station Road, Liverpool" in extracted_text[4]
    assert "Emma Thompson" in extracted_text[5]


def test_extract_text_from_pdf_supplier_agreement_document():
    # Read file bytes and extract text using PDF extractor
    file_bytes = read_file_bytes("supplier_agreement_document.pdf")
    extracted_text = extract_text_from_pdf(file_bytes=file_bytes)

    # Assert all pages extracted
    assert len(extracted_text) == 6

    # Assert page number 1 (first) and number 6 (last) are extracted
    assert 1 in extracted_text
    assert 6 in extracted_text

    # Assert that some key words exist on the correct pages of the extracted text
    assert "Supplier Agreement" in extracted_text[1]
    assert "42 Market Road, London M2 6AB" in extracted_text[2]
    assert "GB991238217" in extracted_text[3]
    assert "GB236106612" in extracted_text[4]
    assert "james.walker@example.co.uk" in extracted_text[5]
    assert "WEST 4000 6247 4508 5472" in extracted_text[6]


def test_extract_text_from_docx_sample_document():
    # Read file bytes and extract text using DOCX extractor
    file_bytes = read_file_bytes("sample_document.docx")
    extracted_text = extract_text_from_docx(file_bytes=file_bytes)

    # Assert that extracted text is dictionary
    assert isinstance(extracted_text, dict)

    # Assert that only one "page", because we treat docx as one single page due to its XML formatting
    assert 1 in extracted_text

    # Assert that the sample name and email has been extracted from the docx file
    assert "Liam Davies" in extracted_text[1]
    assert "liam.davies@example.com" in extracted_text[1]


def test_extract_text_from_txt_sample_notepad():
    # Read file bytes and extract text using TXT extractor
    file_bytes = read_file_bytes("sample_notepad.txt")
    extracted_text = extract_text_from_txt(file_bytes=file_bytes)

    # Assert extracted text is dictionary
    assert isinstance(extracted_text, dict)

    # Assert that only one page because notepad documents only have one page
    assert extracted_text[1]

    # Assert that the sample name and email have been extracte from the txt file
    assert "Emma Thompson" in extracted_text[1]
    assert "emma.thompson@example.com" in extracted_text[1]