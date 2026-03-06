import hashlib
import pymupdf
import spacy
from sqlalchemy.orm import Session
from app.scanning import repository
from app.scanning.models import File, Scan
from app.scanning.regex_patterns import *

# Load the spacy NLP model 
nlp = spacy.load("en_core_web_sm")


# Perform a scan
def perform_scan(db: Session, graph_file_ids: list[str]):
    # Initialise the Scan record
    scan = repository.create_scan(db=db)
    
    for graph_file_id in graph_file_ids:
        try:
            scan_file(db=db, graph_file_id=graph_file_id, scan_id=scan.scan_id)
        except Exception:
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
    scan_file_record = repository.create_scan_file(
        db=db, 
        scan_id=scan_id, 
        graph_file_id=graph_file_id
    )

    # Extract text from fetched file
    file_extracted_text = extract_text_from_pdf(filepath=file_path)

    # Detect sensitive data in file's extracted text
    detections = []

    detections.extend(detect_named_entities(file_extracted_text))
    detections.extend(detect_phone_numbers(file_extracted_text))

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

    print(f'Number of NER detections: {len(detections)}')

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

    print(f'Number of PHONE detections: {len(detections)}')
    
    return detections
            

# Placeholder for dev purposes, returns hard coded test files' paths for testing
def fetch_graph_file(graph_file_id: str):
    match graph_file_id:
        case "abc123":
            return "app/scanning/test_files/client_services_agreement.pdf"
        case "def456":
            return "app/scanning/test_files/confidential_client_list.pdf"
        case "ghi789":
            return "app/scanning/test_files/finance_and_credentials_overview.pdf"
        

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