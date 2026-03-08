from app.scanning.service import (
    extract_text_from_pdf,
    detect_named_entities,
    detect_phone_numbers,
    detect_emails,
    detect_addresses,
    detect_postcodes,
    detect_ibans,
    detect_vats
)


def test_supplier_agreement_contains_phone_detections():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/supplier_agreement_document.pdf")
    detections = detect_phone_numbers(extracted_text)

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
    assert {"sensitivity_subcategory": "PHONE", "page_number": 1} in detections
    assert {"sensitivity_subcategory": "PHONE", "page_number": 2} in detections


def test_operational_report_contains_multiple_email_detections_across_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/operational_report_document.pdf")
    detections = detect_emails(extracted_text)

    assert len(detections) > 1
    assert {"sensitivity_subcategory": "EMAIL", "page_number": 1} in detections
    assert {"sensitivity_subcategory": "EMAIL", "page_number": 2} in detections


def test_operational_report_contains_postcode_detections_on_multiple_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/operational_report_document.pdf")
    detections = detect_postcodes(extracted_text)

    assert len(detections) > 1
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 1} in detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 3} in detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 4} in detections


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

    assert {"sensitivity_subcategory": "PHONE", "page_number": 5} in phone_detections
    assert {"sensitivity_subcategory": "EMAIL", "page_number": 5} in email_detections


def test_realistic_contract_contains_address_and_postcode_detections_across_pages():
    extracted_text = extract_text_from_pdf("tests/scanning_tests/fixtures/realistic_contract_document.pdf")

    address_detections = detect_addresses(extracted_text)
    postcode_detections = detect_postcodes(extracted_text)

    assert len(address_detections) > 1
    assert len(postcode_detections) > 1

    assert {"sensitivity_subcategory": "ADDRESS", "page_number": 2} in address_detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 2} in postcode_detections
    assert {"sensitivity_subcategory": "ADDRESS", "page_number": 5} in address_detections
    assert {"sensitivity_subcategory": "POSTCODE", "page_number": 5} in postcode_detections