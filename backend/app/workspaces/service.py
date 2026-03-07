# Checking workspace creation inputs
def validate_workspace(name:str, image: bytes):

    # Checking if name is null
    if(name is None):
        return "name"
    
    # Checking if image is null
    if(image is None):
        return "image"
    
    return True