import hashlib
import wordninja
import requests
from app.core.security import application

from pathlib import Path
from sqlalchemy.orm import Session
from app.scanning import repository
from app.scanning.models import File, Scan
from app.scanning.schemas import FileResponse

from app.scanning.regex_patterns import *
from app.scanning.detectors import *
from app.scanning.extractors import *
from app.scanning.scan_type import ScanType

from app.ingestion.service import get_download_link_by_graph_id
from app.ingestion.repository import get_ingestion_file_by_graph_id

BASE_DIRECTORY = Path(__file__).resolve().parent


# Perform a scan
def perform_scan(db: Session, graph_file_ids: list[str]):
    # Initialise the Scan record
    scan = repository.create_scan(db=db, scan_type=ScanType.SENSITIVITY)
    
    # Call scan file method for every graph_file_id received (scan_file method will call a method to pull the files)
    for graph_file_id in graph_file_ids:
        try:
            scan_file(db=db, graph_file_id=graph_file_id, scan_id=scan.scan_id)
        except Exception as e:
            print(f"FILE SCAN ERROR: {e}") # Change print to logging in future
            continue

    # Set scan finish time
    repository.end_scan(db=db, scan=scan)

    return {
        "scan_id": scan.scan_id,
        "files_requested": len(graph_file_ids)
    }


# Scan one individual file
def scan_file(db: Session, graph_file_id: str, scan_id: int):

    # Fetch file (for now using the testing method) using its graph_file_id (ingestion component will be integrated here later)
    # file_path = fetch_graph_file(graph_file_id=graph_file_id)

    # Get file's download link via its graph id
    download_url = get_download_link_by_graph_id(application=application(), db=db, graph_id=graph_file_id)

    # Get file's bytes by request, allow for max 2 minutes to not scan empty files / expired links
    file_response = requests.get(download_url, timeout=120)
    file_response.raise_for_status()
    file_bytes = file_response.content

    # Create scan_file record
    file = get_ingestion_file_by_graph_id(db=db, graph_id=graph_file_id)

    # Throw error if file with provided graph file id could not be found
    if file is None:
        raise ValueError(f"File with graph_file_id '{graph_file_id}' not found")

    # Create a scan_file record, linking the file to be scanned with the scan record
    scan_file_record = repository.create_scan_file(
        db=db, 
        scan_id=scan_id, 
        file_id=file.ingestion_file_id
    )

    # Extract text from fetched file
    file_extracted_text = extract_text_from_pdf(file_bytes=file_bytes)

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
    detections.extend(detect_citations(file_extracted_text))
    detections.extend(detect_acts(file_extracted_text))
    detections.extend(detect_regulations(file_extracted_text))
    detections.extend(detect_case_names(file_extracted_text))

    # Create scan_file_detection records for every detection
    for detection in detections:
        repository.create_scan_file_detection(
            db=db, 
            scan_file_id=scan_file_record.scan_file_id,
            sensitivity_subcategory=detection["sensitivity_subcategory"],
            page_number=detection["page_number"]
        )


# Method returns hard coded test files' paths to be used for testing, DO NOT DELETE
def fetch_graph_file(graph_file_id: str):
    test_files_directory = BASE_DIRECTORY / "test_files"

    match graph_file_id:
        case "abc123":
            return test_files_directory / "operational_report_document.pdf"
        case "def456":
            return test_files_directory / "realistic_contract_document.pdf"
        case "ghi789":
            return test_files_directory / "supplier_agreement_document.pdf"
        case "lc111":
            return test_files_directory / "legal_case_report_1.pdf"
        case "lc222":
            return test_files_directory / "legal_case_report_2.pdf"
    

# Get file by id
def get_file(db: Session, file_id: int):
    file = repository.get_file_by_id(db, file_id)

    if file is None:
        return None
    
    return FileResponse(
        file_id = file.ingestion_file_id,
        file_name = file.name,
        hash = file.hash
    )


# Get all scans a file pertains to
def get_file_scans(db: Session, file_id: int):
    return repository.get_file_scans(db, file_id)


# Get latest scan results of a file
def get_file_latest_scan_results(db: Session, file_id: int):
    results = repository.get_latest_scan_detection_summary(db, file_id)
    subcategory_category_map = repository.get_subcategory_category_map(db)

    latest_scan_results = []

    for row in results:
        latest_scan_results.append({
            "category": subcategory_category_map.get(row.sensitivity_subcategory, "Other"),
            "subcategory": row.sensitivity_subcategory,
            "count": row.count
        })

    return latest_scan_results


# Get latest scan results of all files provided in bulk
def get_latest_scan_results_for_files(db: Session, file_ids: list[int]):
    rows = repository.get_latest_scan_detection_summary_for_all_files(db=db, file_ids=file_ids)
    subcategory_category_map = repository.get_subcategory_category_map(db=db)
    
    results_by_file = {}

    # Iterate through all results and append to results_by_file dictionary
    for row in rows:
        if row.file_id not in results_by_file:
            results_by_file[row.file_id] = []

        results_by_file[row.file_id].append({
            "category": subcategory_category_map.get(row.sensitivity_subcategory, "Other"),
            "subcategory": row.sensitivity_subcategory,
            "count": row.count
        })

    return results_by_file


# Get scan status for all files provided in bulk
def get_scan_statuses_for_all_files(db: Session, file_ids: list[int]):
    scanned_file_ids = repository.get_scanned_file_ids(db=db, file_ids=file_ids)
    scanned_file_ids_set = set(scanned_file_ids)

    return {
        file_id: file_id in scanned_file_ids_set
        for file_id in file_ids
    }


# Check if the provided file has been scanned at all
def check_file_has_scan(db: Session, file_id: int):
    return repository.check_file_has_scan(db, file_id)


# Get hash of a file
def get_file_hash(file):
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


def perform_organisation_scan(db: Session, user_id: int, naming_convention_ids: list[int]):

    # Validate the list of naming convention ids
    if not naming_convention_ids:
        raise ValueError("No naming convention(s) selected")
    
    valid_naming_convention_ids = repository.get_naming_convention_ids(db=db)
    for naming_convention_id in naming_convention_ids:
        if naming_convention_id not in valid_naming_convention_ids:
            raise ValueError(f"Invalid naming convention id: {naming_convention_id}")
        
    # Get all files in the user's workspace
    files = repository.get_workspace_files_by_user_id(db=db, user_id=user_id)

    # Don't perform the scan if no files are found
    if len(files) == 0:
        raise ValueError("No files in this workspace")

    scan = repository.create_scan(db=db, scan_type=ScanType.ORGANISATION)

    # Users will be able to select multiple naming conventions on frontend
    for naming_convention_id in naming_convention_ids:
        repository.create_scan_naming_convention(db=db, scan_id=scan.scan_id, naming_convention_id=naming_convention_id)

    # Create a scan_file record for each file
    for file in files:
        repository.create_scan_file(db=db, scan_id=scan.scan_id, file_id=file.ingestion_file_id)

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
        file_name = remove_file_extension(file.name)

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


# Turn repository data into JSON response
def get_scans_with_file_count(db: Session):
    scans = repository.get_scans_with_file_count(db=db)
    return [{
        "scan_id": scan.scan_id, 
        "scan_type": scan.scan_type, 
        "started_at": scan.started_at, 
        "finished_at": scan.finished_at,
        # Gets the number of scan_file records associated with a scan
        "file_count": file_count} 
        for scan, file_count in scans]

def get_scan_by_id(db: Session, scan_id: int):
    return repository.get_scan_by_id(db=db, scan_id=scan_id)

def get_organisational_scan_details(db: Session, scan):
    files = repository.get_scan_files_with_file(db=db, scan_id=scan.scan_id)
    results_query = repository.get_naming_convention_scan_results_by_scan_id(db=db, scan_id=scan.scan_id)

    # Put results_query into dictionary to access when looping
    results = {}

    for naming_convention_scan_result, naming_convention_name, scan_file_id in results_query:
        # Create an empty array if we haven't added any results for this ID yet
        if scan_file_id not in results:
            results[scan_file_id] = []
        
        results[scan_file_id].append({
            "naming_convention_scan_result_id": naming_convention_scan_result.naming_convention_scan_result_id,
            "naming_convention_name": naming_convention_name,
            "passed": naming_convention_scan_result.passed,
            "suggested_name": naming_convention_scan_result.suggested_name
        })

    return {
        "scan_id": scan.scan_id,
        "scan_type": scan.scan_type,
        "started_at": scan.started_at,
        "finished_at": scan.finished_at,
        "file_count": len(files),
        "files": [{
            "scan_file_id": scan_file.scan_file_id,
            "file_id": file.ingestion_file_id,
            "file_name": file.name,
            "hash": file.hash,
            "naming_convention_scan_results": results.get(scan_file.scan_file_id, [])

        } for scan_file, file in files
        ]
    }

def get_sensitivity_scan_details(db: Session, scan):
    files = repository.get_scan_files_with_file(db=db, scan_id=scan.scan_id)

    # Getting total detection counts for each sensitivity category
    detection_counts_query = repository.get_scan_detection_totals_by_scan_id(db=db, scan_id=scan.scan_id)
    categories = repository.get_sensitivity_category_names(db=db)

    detection_counts = {}

    # Loop through categories to create 'detection_counts' entries with 0 as default count
    # Built to allow easy integration of new categories in future
    for category in categories:
        # Format each category key to stay consistent (needed for matching actual count to each category later on)
        key = category.name.lower().replace(" ", "_")
        detection_counts[key] = 0

    for i in detection_counts_query:
        key = i.category_name.lower().replace(" ", "_")
        detection_counts[key] = i.detection_count

    # Same logic as organisational scan results (see above function)
    results_query = repository.get_basic_sensitivity_scan_results_by_scan_id(db=db, scan_id=scan.scan_id)

    results = {}

    for scan_file_id, subcategory_name, category_name in results_query:
        if scan_file_id not in results:
            results[scan_file_id] = []
        
        results[scan_file_id].append({
            "subcategory_name": subcategory_name,
            "category": category_name
        })

    return {
        "scan_id": scan.scan_id,
        "scan_type": scan.scan_type,
        "started_at": scan.started_at,
        "finished_at": scan.finished_at,
        "file_count": len(files),
        "detection_counts": detection_counts,
        "files": [{
            "scan_file_id": scan_file.scan_file_id,
            "file_id": file.ingestion_file_id,
            "file_name": file.name,
            "hash": file.hash,
            "sensitivity_scan_results": results.get(scan_file.scan_file_id, [])
        } for scan_file, file in files
        ]
    }


    

def get_scan_details(db: Session, scan_id: int):
    scan = repository.get_scan_by_id(db=db, scan_id=scan_id)
    
    if not scan:
        return None
    
    if scan.scan_type == ScanType.ORGANISATION:
        return get_organisational_scan_details(db=db, scan=scan)
    
    if scan.scan_type == ScanType.SENSITIVITY:
        return get_sensitivity_scan_details(db=db, scan=scan)
