from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.roles import service

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/get")
def get_roles(db: Session = Depends(get_database)):
    return service.get_roles(db)

@router.post("/create")
def create_role(payload: dict, db: Session = Depends(get_database)):
    """
    payload = {
        "name": "Role Name",
        "thresholds": [
            {"sensitivity_subcategory_id": 1, "threshold": 50},
            ...
        ]
    }
    """
    name = payload.get("name")
    thresholds = payload.get("thresholds", [])
    return service.create_role(db, name, thresholds)

@router.put("/update/{role_id}")
def update_role(role_id: int, payload: dict, db: Session = Depends(get_database)):
    thresholds = payload.get("thresholds", [])
    return service.update_role(db, role_id, thresholds)

@router.delete("/delete/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_database)):
    service.delete_role(db, role_id)
    return {"message": "Role deleted successfully"}

@router.get("/sensitivity/categories")
def get_categories(db: Session = Depends(get_database)):
    return service.get_sensitivity_categories(db)

@router.get("/sensitivity/subcategories")
def get_subcategories(db: Session = Depends(get_database)):
    return service.get_sensitivity_subcategories(db)
