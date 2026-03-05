import hashlib
import wordninja
from sqlalchemy.orm import Session
from app.scanning import repository
from app.scanning.models import File


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


def update_file_hash(db: Session, graph_file_id: str):
    file = repository.get_file_by_graph_id(db=db, graph_file_id=graph_file_id)
    
    # Placeholder, will be replaced by ingestion component's "fetch_file" method when implemented
    graph_file = fetch_graph_file(graph_file_id)

    new_hash = get_file_hash(graph_file)

    repository.set_file_hash(db=db, file=file, new_hash=new_hash)


# Placeholder for dev purposes, returns hard coded test files' paths for testing
def fetch_graph_file(graph_file_id: str):
    match graph_file_id:
        case "abc123":
            return "app/scanning/test_files/client_services_agreement.pdf"
        case "def456":
            return "app/scanning/test_files/confidential_client_list.pdf"
        case "ghi789":
            return "app/scanning/test_files/finance_and_credentials_overview.pdf"

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

# Checks for each naming convention for future use
def is_camel_case(file_name):
    return file_name == to_camel_case(file_name)

def is_snake_case(file_name):
    return file_name == to_snake_case(file_name)

def is_pascal_case(file_name):
    return file_name == to_pascal_case(file_name)

def is_kebab_case(file_name):
    return file_name == to_kebab_case(file_name)

def organisation_scan(db: Session, naming_convention_ids: list[int]):
    scan = repository.create_scan(db=db)
    # Scan all files for now (potentially in future can be selectable)
    files = repository.get_all_files(db=db)

    # User will be able to select multiple naming conventions on frontend
    for naming_convention_id in naming_convention_ids:
        repository.create_scan_naming_convention(db=db, scan_id=scan.scan_id, naming_convention_id=naming_convention_id)

    for file in files:
        repository.create_scan_file(db=db, scan_id=scan.scan_id, file_id=file.file_id)

    scan_files = repository.get_scan_files_by_scan_id(db=db, scan_id=scan.scan_id)

    for scan_file in scan_files:
        file = repository.get_file_by_id(db=db, file_id=scan_file.file_id)

        for naming_convention_id in naming_convention_ids:
            # Naming convention checks
            # ID 1 = camelCase, ID 2 = snake_case, ID 3 = PascalCase, ID 4 = kebab-case
            if naming_convention_id == 1:
                passed = is_camel_case(file.file_name)
                suggested_name = None
                if passed == False:
                    suggested_name = to_camel_case(file.file_name)
            elif naming_convention_id == 2:
                passed = is_snake_case(file.file_name)
                suggested_name = None
                if passed == False:
                    suggested_name = to_snake_case(file.file_name)
            elif naming_convention_id == 3:
                passed = is_pascal_case(file.file_name)
                suggested_name = None
                if passed == False:
                    suggested_name = to_pascal_case(file.file_name)
            elif naming_convention_id == 4:
                passed = is_kebab_case(file.file_name)
                suggested_name = None
                if passed == False:
                    suggested_name = to_kebab_case(file.file_name)

            repository.set_naming_convention_scan_result(db=db, scan_file_id=scan_file.scan_file_id, scan_naming_convention_id=naming_convention_id, passed=passed, suggested_name=suggested_name)

