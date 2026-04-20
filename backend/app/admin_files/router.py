from fastapi import APIRouter, Query
from app.admin_files import service

router = APIRouter(prefix="/admin/files", tags=["Admin Files"])


@router.get("")
def get_admin_files(
    search: str = "",
    sensitivity: str = "",
    sort: str = "desc",
    page: int = 1,
    page_size: int = 20,
):
    return service.get_admin_files(
        search=search,
        sensitivity=sensitivity,
        sort=sort,
        page=page,
        page_size=page_size,
    )