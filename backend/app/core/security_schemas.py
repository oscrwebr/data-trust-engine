from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    user_id: int
    # role: # This can be implemented when/if needed easily - ensure to discuss and implement early if required