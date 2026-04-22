from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_database
from app.admin_files import service

router = APIRouter(prefix="/admin/files", tags=["Admin Files"])


@router.get("/last-scanned")
def get_last_scanned(
    file_ids: List[int] = Query(...),
    db: Session = Depends(get_database)
):
    return service.get_last_scanned(db, file_ids)
    