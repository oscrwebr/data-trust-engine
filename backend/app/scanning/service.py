import hashlib
from app.scanning import repository


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


def update_file_hash(graph_file_id):
    file = repository.get_file_by_graph_id(graph_file_id)
    
    # Placeholder, will be replaced by ingestion component's "fetch_file" method when implemented
    graph_file = fetch_graph_file(graph_file_id)

    new_hash = get_file_hash(graph_file)

    repository.set_file_hash(file=file, new_hash=new_hash)


# Placeholder for dev purposes, returns hard coded test files' paths for testing
def fetch_graph_file(graph_file_id):
    match graph_file_id:
        case "abc123":
            return "app\scanning\test_files\client_services_agreement.pdf"
        case "def456":
            return "app\scanning\test_files\confidential_client_list.pdf"
        case "ghi789":
            return "app\scanning\test_files\finance_and_credentials_overview.pdf"