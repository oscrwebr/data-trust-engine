from app.scanning.extractors import *
from app.scanning.detectors import *


def test_supplier_agreement_contains_phone_detections():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/supplier_agreement_document.pdf")
    detections = detect_phone_numbers(extracted_text)

    print(extracted_text)

    # Assert that detections are made for PHONE
    assert len(detections) > 0
    assert all(detection["sensitivity_subcategory"] == "PHONE" for detection in detections)


def test_supplier_agreement_contains_email_detections():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/supplier_agreement_document.pdf")
    detections = detect_emails(extracted_text)

    # Assert that detections are made for EMAIL
    assert len(detections) > 0
    assert all(detection["sensitivity_subcategory"] == "EMAIL" for detection in detections)


def test_operational_report_contains_name_and_address_detections():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/operational_report_document.pdf")

    name_detections = detect_named_entities(extracted_text)
    address_detections = detect_addresses(extracted_text)

    assert len(name_detections) > 0
    assert len(address_detections) > 0

    assert all(detection["sensitivity_subcategory"] == "NAME" for detection in name_detections)
    assert all(detection["sensitivity_subcategory"] == "ADDRESS" for detection in address_detections)


def test_operational_report_contains_multiple_phone_detections_across_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/operational_report_document.pdf")
    detections = detect_phone_numbers(extracted_text)

    assert len(detections) > 1
    assert {"sensitivity_subcategory": "PHONE", "page_number": 1, "matched_text": "+44 7700 90305"} in detections
    assert {"sensitivity_subcategory": "PHONE", "page_number": 2, "matched_text": "+44 7700 90267"} in detections


def test_operational_report_contains_multiple_email_detections_across_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/operational_report_document.pdf")
    detections = detect_emails(extracted_text)

    assert len(detections) > 1
    assert {"sensitivity_subcategory": "EMAIL", "page_number": 1, "matched_text": "oliver.hughes@example.co.uk"} in detections
    assert {"sensitivity_subcategory": "EMAIL", "page_number": 2, "matched_text": "james.walker@northbridge-consulting.co.uk"} in detections


def test_operational_report_contains_postcode_detections_on_multiple_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/operational_report_document.pdf")
    detections = detect_postcodes(extracted_text)

    assert len(detections) > 1
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 1, "matched_text": "CF10 3AT"} in detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 3, "matched_text": "NW1 6XE"} in detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 4, "matched_text": "SW1A 2AA"} in detections


def test_supplier_agreement_contains_iban_and_vat_detections():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/supplier_agreement_document.pdf")

    iban_detections = detect_ibans(extracted_text)
    vat_detections = detect_vats(extracted_text)

    assert len(iban_detections) > 0
    assert len(vat_detections) > 0

    assert all(detection["sensitivity_subcategory"] == "IBAN" for detection in iban_detections)
    assert all(detection["sensitivity_subcategory"] == "VAT" for detection in vat_detections)


def test_supplier_agreement_contains_multiple_name_detections_across_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/supplier_agreement_document.pdf")
    detections = detect_named_entities(extracted_text)

    assert len(detections) > 1
    assert {"sensitivity_subcategory": "NAME", "page_number": 1} in detections
    assert {"sensitivity_subcategory": "NAME", "page_number": 3} in detections
    assert {"sensitivity_subcategory": "NAME", "page_number": 5} in detections


def test_supplier_agreement_contains_address_and_postcode_detections():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/supplier_agreement_document.pdf")

    address_detections = detect_addresses(extracted_text)
    postcode_detections = detect_postcodes(extracted_text)

    assert len(address_detections) > 0
    assert len(postcode_detections) > 0

    assert all(detection["sensitivity_subcategory"] == "ADDRESS" for detection in address_detections)
    assert all(detection["sensitivity_subcategory"] == "POSTCODE" for detection in postcode_detections)


def test_realistic_contract_contains_multiple_detector_types():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/realistic_contract_document.pdf")

    name_detections = detect_named_entities(extracted_text)
    phone_detections = detect_phone_numbers(extracted_text)
    email_detections = detect_emails(extracted_text)
    iban_detections = detect_ibans(extracted_text)
    vat_detections = detect_vats(extracted_text)

    assert len(name_detections) > 0
    assert len(phone_detections) > 0
    assert len(email_detections) > 0
    assert len(iban_detections) > 0
    assert len(vat_detections) > 0


def test_realistic_contract_contains_detections_on_last_page():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/realistic_contract_document.pdf")

    phone_detections = detect_phone_numbers(extracted_text)
    email_detections = detect_emails(extracted_text)

    assert {"sensitivity_subcategory": "PHONE", "page_number": 5, "matched_text": "+44 7700 90532"} in phone_detections
    assert {"sensitivity_subcategory": "EMAIL", "page_number": 5, "matched_text": "sophia.patel@finance-demo.co.uk"} in email_detections


def test_realistic_contract_contains_address_and_postcode_detections_across_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/realistic_contract_document.pdf")

    address_detections = detect_addresses(extracted_text)
    postcode_detections = detect_postcodes(extracted_text)

    assert len(address_detections) > 1
    assert len(postcode_detections) > 1

    assert {"sensitivity_subcategory": "ADDRESS", "page_number": 2, "matched_text": "18 Station Road"} in address_detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 2, "matched_text": "SW1A 2AA"} in postcode_detections
    assert {"sensitivity_subcategory": "ADDRESS", "page_number": 5, "matched_text": "14 King Street"} in address_detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 5, "matched_text": "B1 1AA"} in postcode_detections


def test_legal_case_report_1_contains_citations_and_acts_and_case_names():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/legal_case_report_1.pdf")

    citation_detections = detect_citations(extracted_text)
    act_detections = detect_acts(extracted_text)
    case_name_detections = detect_case_names(extracted_text)

    # This PDF file should have exactly 9 citation detections
    assert len(citation_detections) == 9

    # This PDF file should have exactly 3 act detections
    assert len(act_detections) == 3

    # This PDF file should have exactly 24 case name detections
    assert len(case_name_detections) == 24

    # Ensure specific piece of information are picked up as citation detections
    assert {"sensitivity_subcategory": "CITATION", "page_number": 1, "matched_text": "[2026] EWCA Civ 19"} in citation_detections
    assert {"sensitivity_subcategory": "CITATION", "page_number": 13, "matched_text": "[2021] UKSC 16"} in citation_detections
    assert {"sensitivity_subcategory": "CITATION", "page_number": 18, "matched_text": "[2016] EWHC 1370"} in citation_detections

    # Ensure specific piece of information are picked up as act detections
    assert {"sensitivity_subcategory": "ACT", "page_number": 2, "matched_text": "Welfare Reform Act 2007"} in act_detections
    assert {"sensitivity_subcategory": "ACT", "page_number": 7, "matched_text": "Benefits Act 1992"} in act_detections
    assert {"sensitivity_subcategory": "ACT", "page_number": 13, "matched_text": "Welfare Reform Act 2007"} in act_detections

    # Ensure specific piece of information are picked up as case name detections
    assert {"sensitivity_subcategory": "CASE_NAME", "page_number": 4, "matched_text": "Allen v Secretary"} in case_name_detections
    assert {"sensitivity_subcategory": "CASE_NAME", "page_number": 11, "matched_text": "Iman Alhashem v The Secretary"} in case_name_detections
    assert {"sensitivity_subcategory": "CASE_NAME", "page_number": 13, "matched_text": "Rossendale Borough Council v Hurstwood Properties"} in case_name_detections


def test_legal_case_report_2_contains_citations_and_acts_and_case_names():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/legal_case_report_2.pdf")

    citation_detections = detect_citations(extracted_text)
    act_detections = detect_acts(extracted_text)
    case_name_detections = detect_case_names(extracted_text)

    # This PDF file should have exactly 7 citation detections
    assert len(citation_detections) == 7

    # This PDF file should have exactly 15 act detections
    assert len(act_detections) == 15

    # This PDF file should have exactly 3 case name detections
    assert len(case_name_detections) == 3

    # Ensure specific piece of information are picked up as citation detections
    assert {"sensitivity_subcategory": "CITATION", "page_number": 1, "matched_text": "[2020] EWCA Civ 1"} in citation_detections
    assert {"sensitivity_subcategory": "CITATION", "page_number": 11, "matched_text": "[2018] UKSC 61"} in citation_detections
    assert {"sensitivity_subcategory": "CITATION", "page_number": 27, "matched_text": "[2018] EWHC 3251"} in citation_detections

    # Ensure specific piece of information are picked up as act detections
    assert {"sensitivity_subcategory": "ACT", "page_number": 3, "matched_text": "Social Security Pensions Act 1975"} in act_detections
    assert {"sensitivity_subcategory": "ACT", "page_number": 14, "matched_text": "Pensions Act 2014"} in act_detections
    assert {"sensitivity_subcategory": "ACT", "page_number": 27, "matched_text": "Pension Schemes Act 1993"} in act_detections

    # Ensure specific piece of information are picked up as case name detections
    assert {"sensitivity_subcategory": "CASE_NAME", "page_number": 11, "matched_text": "In Henderson v Foxworth Investments Ltd"} in case_name_detections
    assert {"sensitivity_subcategory": "CASE_NAME", "page_number": 11, "matched_text": "In Volcafe Ltd v Cia Sud America"} in case_name_detections
    assert {"sensitivity_subcategory": "CASE_NAME", "page_number": 11, "matched_text": "In Smech Properties Ltd v Runnymede Borough Council"} in case_name_detections


