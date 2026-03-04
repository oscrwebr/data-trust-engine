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
    camel_case_name = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    return camel_case_name

def to_snake_case(file_name):
    words = split_file_name(file_name)
    snake_case_name = '_'.join(word.lower() for word in words)
    return snake_case_name

def to_kebab_case(file_name):
    words = split_file_name(file_name)
    kebab_case_name = '-'.join(word.lower() for word in words)
    return kebab_case_name
