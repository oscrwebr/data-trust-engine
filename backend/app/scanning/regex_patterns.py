import re

UK_PHONE_REGEX = re.compile(
    r"\b(?:\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}\b"
)

EMAIL_REGEX = re.compile(
    r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b"
)

UK_POSTCODE_REGEX = re.compile(
    r"\b(GIR\s?0AA|"
    r"(?:[A-PR-UWYZ][0-9]{1,2}"
    r"|[A-PR-UWYZ][A-HK-Y][0-9]{1,2}"
    r"|[A-PR-UWYZ][0-9][A-HJKS-UW]"
    r"|[A-PR-UWYZ][A-HK-Y][0-9][ABEHMNPRV-Y])"
    r"\s?[0-9][ABD-HJLNP-UW-Z]{2})\b",
    re.IGNORECASE
)