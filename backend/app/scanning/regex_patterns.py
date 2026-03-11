import re

# Personally identifying information patterns
UK_PHONE_REGEX = re.compile(
    r"(\+44\s?7\d{3}\s?\d{5,6}|\+44\s?\d{4}\s?\d{5,6}|07\d{3}\s?\d{6}|0\d{4}\s?\d{6})"
)

EMAIL_REGEX = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

ADDRESS_REGEX = re.compile(
    r"\b\d{1,4}[A-Za-z]?\s+[A-Za-z\s]{3,30}\s(?:Street|St|Road|Rd|Lane|Ln|Avenue|Ave|Drive|Dr|Close|Way)\b",
    re.IGNORECASE
)

UK_POSTCODE_REGEX = re.compile(
    r"\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b",
    re.IGNORECASE
)


# Financial information patterns
IBAN_REGEX = re.compile(
    r"\b[A-Z]{2}\d{2}[ ]?[A-Z0-9]{4}[ ]?[A-Z0-9]{4}[ ]?[A-Z0-9]{4}[ ]?[A-Z0-9]{4}[ ]?[A-Z0-9]{0,4}\b"
)

UK_VAT_REGEX = re.compile(
    r"\b(?:GB)?\d{3}\s?\d{4}\s?\d{2}\b"
)


# Legal case information patterns
CITATION_REGEX = re.compile(
    r"\[\d{4}\]\s+[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*)*\s+\d+"
)

ACT_REGEX = re.compile(
    r"\b[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*)*\s+Act\s+\d{4}\b"
)

REGULATION_REGEX = re.compile(
    r"\b(Regulation\s*\([A-Z]{2,}\)\s*\d{4}/\d+|UK GDPR|GDPR)\b"
)

CASE_NAME_REGEX = re.compile(
    r"\b[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*)*\s+v\.?\s+[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*)*"
)