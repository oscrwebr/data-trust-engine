from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.org_chart.service import parse_orgchart_file, confirm_orgchart
from app.core.database import get_database
from app.workspaces.repository import get_workspace_by_user
from ..core.security import get_user_from_access_token
from ..core.security_schemas import User

router = APIRouter(prefix="/org-chart", tags=["org-chart"])


@router.post("/parse-orgchart")
async def parse_orgchart(orgChart: UploadFile = File(...)):
    """
    Upload Excel/CSV file and parse into roles and employees
    """
    result = await parse_orgchart_file(orgChart)
    return result


@router.post("/confirm-orgchart")
async def confirm_orgchart_roles(
    data: dict, 
    db: Session = Depends(get_database),
    current_user: User = Depends(get_user_from_access_token)
):
    """
    Accept parsed roles and save them into DB
    """
    workspace_id = get_workspace_by_user(db, current_user.user_id)
    result = await confirm_orgchart(data["roles"], db, workspace_id)
    return {"status": "success", "roles": result}