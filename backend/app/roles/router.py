from fastapi import APIRouter

router = APIRouter(prefix="/roles")

@router.get("/get")
def get_roles():
    return [{"id": 1, "name": "PII"}, {"id": 2, "name": "Legal"}, {"id": 3, "name": "Financial"}]
