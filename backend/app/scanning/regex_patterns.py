import re

UK_PHONE_REGEX = re.compile(
    r"(?:\+44\s?7\d{3}|\(?07\d{3}\)?)[\s-]?\d{3}[\s-]?\d{3}"
)

EMAIL_REGEX = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

UK_POSTCODE_REGEX = re.compile(
    r"\b([A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2})\b",
    re.IGNORECASE
)