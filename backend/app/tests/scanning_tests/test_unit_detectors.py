from app.scanning.detectors import *


def test_detects_named_entities():
    text_dict = {
        1: "Sarah Mitchell attended the meeting.",
        2: "This string should not be detected",
        3: "Daniel Carter approved the contract."
    }

    detections = detect_named_entities(text_dict=text_dict)

    assert len(detections) >= 2
    assert detections[0]["sensitivity_subcategory"] == "NAME"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "NAME"
    assert detections[1]["page_number"] == 3


def test_detects_phone_numbers():
    text_dict = {
        1: "Call Bob on +44 1234 123456",
        2: "Alternative number on 07700 987654",
        3: "This string should not be detected"
    }

    detections = detect_phone_numbers(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "PHONE"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "PHONE"
    assert detections[1]["page_number"] == 2


def test_detects_emails():
    text_dict = {
        1: "Contact Bob at bob.smith@example.com",
        2: "This string should not be detected",
        3: "Alternative address: alice.jones@test.co.uk"
    }

    detections = detect_emails(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "EMAIL"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "EMAIL"
    assert detections[1]["page_number"] == 3


def test_detects_addresses():
    text_dict = {
        1: "The office is located at 221 Baker Street",
        2: "Registered address is 14 King Street",
        3: "This string should not be detected"
    }

    detections = detect_addresses(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "ADDRESS"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "ADDRESS"
    assert detections[1]["page_number"] == 2


def test_detects_postcodes():
    text_dict = {
        1: "This string should not be detected",
        2: "The London office postcode is SW1A 2AA",
        3: "The Cardiff office postcode is CF10 3AT"
    }

    detections = detect_postcodes(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "POSTCODE"
    assert detections[0]["page_number"] == 2
    assert detections[1]["sensitivity_subcategory"] == "POSTCODE"
    assert detections[1]["page_number"] == 3


def test_detects_ibans():
    text_dict = {
        1: "Payment should be made to IBAN GB82 WEST 1234 5698 7654 32",
        2: "Alternative account is DE89 3704 0044 0532 0130 00",
        3: "This string should not be detected"
    }

    detections = detect_ibans(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "IBAN"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "IBAN"
    assert detections[1]["page_number"] == 2


def test_detects_vats():
    text_dict = {
        1: "The VAT registration is GB123456789",
        2: "Alternative VAT number is GB987654321",
        3: "This string should not be detected"
    }

    detections = detect_vats(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "VAT"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "VAT"
    assert detections[1]["page_number"] == 2


def test_detects_citations():
    text_dict = {
        1: "This is a valid citation [2026] AC 690",
        2: "This string should not be detected",
        3: "This citation [2016] EWCA Civ 395 should also be detected",
    }

    detections = detect_citations(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "CITATION"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "CITATION"
    assert detections[1]["page_number"] == 3


def test_detect_acts():
    text_dict = {
        1: "This is not an act detection",
        2: "The act Benefits Act 1992 was used in this string",
        3: "Welfare Reform Act 2004 should be detected"
    }

    detections = detect_acts(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "ACT"
    assert detections[0]["page_number"] == 2
    assert detections[1]["sensitivity_subcategory"] == "ACT"
    assert detections[1]["page_number"] == 3


def test_detect_regulations():
    text_dict = {
        1: "This is not a regulation detection",
        2: "The document refers to Regulation (EU) 2016/679.",
        3: "Another valid one is Regulation (UK) 2024/1021 in this text",
    }

    detections = detect_regulations(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "REGULATION"
    assert detections[0]["page_number"] == 2
    assert detections[1]["sensitivity_subcategory"] == "REGULATION"
    assert detections[1]["page_number"] == 3


def test_detect_case_names():
    text_dict = {
        1: "This case is regarding the case of Vodaphone v Sky",
        2: "Smech Properties Ltd v Runnymede Borough Council is another valid detection",
        3: "There is no case name to be detected in this string"
    }

    detections = detect_case_names(text_dict=text_dict)

    assert len(detections) == 2
    assert detections[0]["sensitivity_subcategory"] == "CASE_NAME"
    assert detections[0]["page_number"] == 1
    assert detections[1]["sensitivity_subcategory"] == "CASE_NAME"
    assert detections[1]["page_number"] == 2