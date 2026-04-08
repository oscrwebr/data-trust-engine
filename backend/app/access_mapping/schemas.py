from pydantic import BaseModel


class FileEmployeeAccessResponse(BaseModel):
    user_id: int
    name: str
    email: str
    roles: list[str]