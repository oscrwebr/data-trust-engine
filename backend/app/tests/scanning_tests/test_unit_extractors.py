from app.scanning.extractors import *


def test_extract_text_from_pdf_operational_report_document():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/operational_report_document.pdf")
    
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
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/realistic_contract_document.pdf")

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
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/supplier_agreement_document.pdf")

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