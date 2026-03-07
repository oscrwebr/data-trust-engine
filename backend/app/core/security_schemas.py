from pydantic import BaseModel
from datetime import datetime

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    opaque_token: str
    hashed_ot: str
    expiry_date: datetime
    
class User(BaseModel):
    user_id: int
    # role: # This can be implemented when/if needed easily - ensure to discuss and implement early if required