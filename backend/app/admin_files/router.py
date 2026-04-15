# app/admin_files/router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.core.security import get_user_from_access_token
from app.admin_files import service

router = APIRouter(prefix="/admin/files", tags=["Admin Files"])


@router.get("/")
def get_admin_files(
    db: Session = Depends(get_database),
    user = Depends(get_user_from_access_token),
    search: str = Query(None),
    sensitivity: str = Query(None),  # high | low
    sort: str = Query("desc"),       # asc | desc
    page: int = Query(1),
    page_size: int = Query(20)
):
    # 🔐 enforce admin
    if user.role != "admin":
        return {"error": "Unauthorized"}

    return service.get_admin_files(
        db,
        search,
        sensitivity,
        sort,
        page,
        page_size
    )