import hashlib
import pymupdf
import spacy
import wordninja
from sqlalchemy.orm import Session
from app.scanning import repository
from app.scanning.models import File, Scan
from app.scanning.regex_patterns import *

import lexnlp.extract.en.citations as nlp_citations
import lexnlp.extract.en.regulations as nlp_regulations
import lexnlp.extract.en.courts as nlp_courts
import lexnlp.extract.en.acts as nlp_acts

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")


# Perform a scan
def perform_scan(db: Session, graph_file_ids: list[str]):
    # Initialise the Scan record
    scan = repository.create_scan(db=db)
    
    for graph_file_id in graph_file_ids:
        try:
            scan_file(db=db, graph_file_id=graph_file_id, scan_id=scan.scan_id)
        except Exception as e:
            print(f"FILE SCAN ERROR: {e}")
            continue

    return {
        "scan_id": scan.scan_id,
        "files_requested": len(graph_file_ids)
    }


# Scan one individual file
def scan_file(db: Session, graph_file_id: str, scan_id: int):

    # Fetch file (for now a hardcoded file path) using its graph_file_id (ingestion component will be integrated here later)
    file_path = fetch_graph_file(graph_file_id=graph_file_id)

    # Create scan_file record
    file = repository.get_file_by_graph_id(db=db, graph_file_id=graph_file_id)

    if file is None:
        raise ValueError(f"File with graph_file_id '{graph_file_id}' not found")

    scan_file_record = repository.create_scan_file(
        db=db, 
        scan_id=scan_id, 
        file_id=file.file_id
    )

    # Extract text from fetched file
    file_extracted_text = extract_text_from_pdf(filepath=file_path)

    # Detect sensitive data in file's extracted text
    detections = []

    # Detection of PII (Personally Identifiable Information) information
    detections.extend(detect_named_entities(file_extracted_text))
    detections.extend(detect_phone_numbers(file_extracted_text))
    detections.extend(detect_emails(file_extracted_text))
    detections.extend(detect_addresses(file_extracted_text))
    detections.extend(detect_postcodes(file_extracted_text))

    # Detection of financial information
    detections.extend(detect_ibans(file_extracted_text))
    detections.extend(detect_vats(file_extracted_text))

    # Detection of legal case information
    detections.extend(detect_case_names((file_extracted_text)))

    # Create scan_file_detection records for every detection
    for detection in detections:
        repository.create_scan_file_detection(
            db=db, 
            scan_file_id=scan_file_record.scan_file_id,
            sensitivity_subcategory=detection["sensitivity_subcategory"],
            page_number=detection["page_number"]
        )


# Extract text from PDF into dict
def extract_text_from_pdf(filepath: str) -> dict:
    file = pymupdf.open(filepath)
    extracted_text = {}

    # Make page numbers 1 indexed, because user think in page 1, 2, 3 not 0, 1, 2
    for page_number in range(len(file)):
        page = file.load_page(page_number)
        text = page.get_text("text")
        
        # Normalisation to remove line breaks
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()

        extracted_text[page_number + 1] = text

    file.close()
    return extracted_text


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


# Phone number detection using regex
def detect_phone_numbers(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        for match in UK_PHONE_REGEX.finditer(text):
            detections.append({
                "sensitivity_subcategory": "PHONE",
                "page_number": page_number
            })

            print(f'PHONE detection: {match.group()} | PAGE: {page_number}')

    return detections


# Email detection using regex
def detect_emails(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        for match in EMAIL_REGEX.finditer(text):
            detections.append({
                "sensitivity_subcategory": "EMAIL",
                "page_number": page_number
            })

            print(f'EMAIL detection: {match.group()} | PAGE: {page_number}')

    return detections


# Address detection using regex
def detect_addresses(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        for match in ADDRESS_REGEX.finditer(text):
            detections.append({
                "sensitivity_subcategory": "ADDRESS",
                "page_number": page_number
            })

            print(f'ADDRESS detection: {match.group()} | PAGE: {page_number}')

    return detections


# Postcode detection using regex
def detect_postcodes(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        for match in UK_POSTCODE_REGEX.finditer(text):
            detections.append({
                "sensitivity_subcategory": "POSTCODE",
                "page_number": page_number
            })

            print(f'POSTCODE detection: {match.group()} | PAGE: {page_number}')

    return detections


# IBAN detection using regex
def detect_ibans(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        for match in IBAN_REGEX.finditer(text):
            detections.append({
                "sensitivity_subcategory": "IBAN",
                "page_number": page_number
            })

            print(f'IBAN detection: {match.group()} | PAGE: {page_number}')

    return detections


# VAT detection using regex
def detect_vats(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        for match in UK_VAT_REGEX.finditer(text):
            detections.append({
                "sensitivity_subcategory": "VAT",
                "page_number": page_number
            })

            print(f'VAT detection: {match.group()} | PAGE: {page_number}')
    
    return detections


## LEGAL CATEGORY SENSITIVE DATA DETECTION
def detect_citations(text_dict):
    detections = []

    for page_number, text in text_dict.items():
        for citation in nlp_citations.get_citations(text):
            detections.append({
                "sensitivity_subcategory": "CITATION",
                "page_number": page_number
            })


    # for page_number, text in text_dict.items():
    #     doc = nlp(text)

    #     for entity in doc.ents:
    #         if entity.label_ == "PERSON":
    #             detections.append({
    #                 "sensitivity_subcategory": "NAME",
    #                 "page_number": page_number
    #             })

    #             print(f'PERSON detection: {entity} | PAGE: {page_number}')

    # return detections

# Placeholder for dev purposes, returns hard coded test files' paths for testing
def fetch_graph_file(graph_file_id: str):
    match graph_file_id:
        case "abc123":
            return "app/scanning/test_files/operational_report_document.pdf"
        case "def456":
            return "app/scanning/test_files/realistic_contract_document.pdf"
        case "ghi789":
            return "app/scanning/test_files/supplier_agreement_document.pdf"
        

def get_file_hash(file: File):
    # Create hash object
    hash = hashlib.sha256()

    # Read file in binary mode
    with open(file, "rb") as file:
        
        # Loop until end of file, reading 1024 bytes at a time
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            hash.update(chunk)

    # Return hash
    return hash.hexdigest()


# Update hash of file 
def update_file_hash(db: Session, graph_file_id: str):
    file = repository.get_file_by_graph_id(db=db, graph_file_id=graph_file_id)
    
    # Placeholder, will be replaced by ingestion component's "fetch_file" method when implemented
    graph_file = fetch_graph_file(graph_file_id)

    new_hash = get_file_hash(graph_file)

    repository.set_file_hash(db=db, file=file, new_hash=new_hash)

# All naming convention methods use the Word Ninja library to split file names into English words
# https://github.com/keredson/wordninja
def split_file_name(file_name):
    return wordninja.split(file_name)

def to_camel_case(file_name):
    words = split_file_name(file_name)
    # Keep the first word lowercase and then capitalise the next words
    camel_case_name = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    return camel_case_name

def to_snake_case(file_name):
    words = split_file_name(file_name)
    # Keep all words lowercase and join with underscores
    snake_case_name = '_'.join(word.lower() for word in words)
    return snake_case_name

def to_pascal_case(file_name):
    words = split_file_name(file_name)
    # Capitalise all words
    pascal_case_name = ''.join(word.capitalize() for word in words)
    return pascal_case_name

def to_kebab_case(file_name):
    words = split_file_name(file_name)
    # Keep all words lowercase and join with hyphens
    kebab_case_name = '-'.join(word.lower() for word in words)
    return kebab_case_name

# Checks for each naming convention
def is_camel_case(file_name):
    return file_name == to_camel_case(file_name)

def is_snake_case(file_name):
    return file_name == to_snake_case(file_name)

def is_pascal_case(file_name):
    return file_name == to_pascal_case(file_name)

def is_kebab_case(file_name):
    return file_name == to_kebab_case(file_name)

def remove_file_extension(file_name):
    return file_name.rsplit('.', 1)[0]

def perform_organisation_scan(db: Session, naming_convention_ids: list[int]):

    # Validate the list of naming convention ids
    if not naming_convention_ids:
        raise ValueError("No naming convention(s) selected")
    
    valid_naming_convention_ids = repository.get_naming_convention_ids(db=db)
    for naming_convention_id in naming_convention_ids:
        if naming_convention_id not in valid_naming_convention_ids:
            raise ValueError(f"Invalid naming convention id: {naming_convention_id}")

    scan = repository.create_scan(db=db)
    # Scan all files for now (potentially in future can be selectable)
    files = repository.get_all_files(db=db)

    # Users will be able to select multiple naming conventions on frontend
    for naming_convention_id in naming_convention_ids:
        repository.create_scan_naming_convention(db=db, scan_id=scan.scan_id, naming_convention_id=naming_convention_id)

    # Create a scan_file record for each file
    for file in files:
        repository.create_scan_file(db=db, scan_id=scan.scan_id, file_id=file.file_id)

    # Get the naming conventions for this scan
    scan_naming_conventions = repository.get_scan_naming_convention_by_scan_id(db=db, scan_id=scan.scan_id)

    # Join query to get scan files with their corresponding file table data
    scan_files = repository.get_scan_files_with_file(db=db, scan_id=scan.scan_id)


    # Optimising if/elif code blocks adapted from:
    # https://www.reddit.com/r/learnpython/comments/iq5qhl/most_efficient_way_to_do_lots_of_ifelif_statements/
    naming_convention_checks = {
        1: is_camel_case,
        2: is_snake_case,
        3: is_pascal_case,
        4: is_kebab_case
    }

    naming_convention_suggestions = {
        1: to_camel_case,
        2: to_snake_case,
        3: to_pascal_case,
        4: to_kebab_case
    }

    for scan_file, file in scan_files:

        # As file names will be stored with their extension, this removes the extension for naming convention checks
        file_name = remove_file_extension(file.file_name)

        for scan_naming_convention in scan_naming_conventions:
            checks = naming_convention_checks.get(scan_naming_convention.naming_convention_id)
            suggestions = naming_convention_suggestions.get(scan_naming_convention.naming_convention_id)

            if checks is None or suggestions is None:
                continue

            passed = checks(file_name)
            suggested_name = None
            if passed == False:
                suggested_name = suggestions(file_name)
                
            repository.set_naming_convention_scan_result(db=db, scan_file_id=scan_file.scan_file_id, scan_naming_convention_id=scan_naming_convention.scan_naming_convention_id, passed=passed, suggested_name=suggested_name)
    repository.end_scan(db=db, scan=scan)
    return scan
