import spacy

from app.scanning.regex_patterns import *

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_lg")


# Named entity recognition detection (names, organisations) using spacy nlp model
def detect_named_entities(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        doc = nlp(text)

        for entity in doc.ents:
            if entity.label_ == "PERSON":
                detections.append({
                    "sensitivity_subcategory": "NAME",
                    "page_number": page_number
                })

                print(f'PERSON detection: {entity} | PAGE: {page_number}')

    return detections


# Regex pattern detection helper method
def detect_with_regex(detection_subcategory, detection_regex, text_dict):
    detections = []

    # Iterate through the text of each page, find regex matches and append to detections array
    for page_number, text in text_dict.items():
        for match in detection_regex.finditer(text):
            detections.append({
                "sensitivity_subcategory": detection_subcategory,
                "page_number": page_number
            })

            print(f"{detection_subcategory} detection: {match.group()} | PAGE: {page_number}")

    return detections


# Phone number detection
def detect_phone_numbers(text_dict):
    return detect_with_regex("PHONE", UK_PHONE_REGEX, text_dict)


# Email detection using regex
def detect_emails(text_dict):
    return detect_with_regex("EMAIL", EMAIL_REGEX, text_dict)


# Address detection using regex
def detect_addresses(text_dict):
    return detect_with_regex("ADDRESS", ADDRESS_REGEX, text_dict)


# Postcode detection using regex
def detect_postcodes(text_dict):
    return detect_with_regex("POSTCODE", UK_POSTCODE_REGEX, text_dict)


# IBAN detection using regex
def detect_ibans(text_dict):
    return detect_with_regex("IBAN", IBAN_REGEX, text_dict)


# VAT detection using regex
def detect_vats(text_dict):
    return detect_with_regex("VAT", UK_VAT_REGEX, text_dict)


# Legal citation detection using regex
def detect_citations(text_dict):
    return detect_with_regex("CITATION", CITATION_REGEX, text_dict)


# Legal act detection using regex
def detect_acts(text_dict):
    return detect_with_regex("ACT", ACT_REGEX, text_dict)


# Legal regulation detection using regex
def detect_regulations(text_dict):
    return detect_with_regex("REGULATION", REGULATION_REGEX, text_dict)


# Legal case name detection using regex
def detect_case_names(text_dict):
    return detect_with_regex("CASE_NAME", CASE_NAME_REGEX, text_dict)