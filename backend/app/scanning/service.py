from .schemas import ScanRequest, ScanResponse
import hashlib

def hash_file(file):
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