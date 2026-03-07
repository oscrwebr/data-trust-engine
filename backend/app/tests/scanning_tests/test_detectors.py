from app.scanning.service import (
    detect_named_entities,
    detect_phone_numbers,
    detect_emails,
    detect_addresses,
    detect_postcodes,
    detect_ibans,
    detect_vats
)


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