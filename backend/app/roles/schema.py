from fastapi import FastAPI
from pydantic import BaseModel
from app.authentication.models import User
from typing import List

app = FastAPI()

class EmployeeRoleUpdate(BaseModel):
    user_id: int
    role_name: str

class UpdateUserRolesRequest(BaseModel):
    employees: List[EmployeeRoleUpdate]