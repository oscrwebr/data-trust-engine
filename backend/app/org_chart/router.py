from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.org_chart.service import parse_orgchart_file, confirm_orgchart
from app.core.database import get_database

router = APIRouter(prefix="/org-chart", tags=["org-chart"])


@router.post("/parse-orgchart")
async def parse_orgchart(orgChart: UploadFile = File(...)):
    """
    Upload Excel/CSV file and parse into roles and employees
    """
    result = await parse_orgchart_file(orgChart)
    return result


@router.post("/confirm-orgchart")
def confirm_orgchart_roles(
    data: dict, 
    db: Session = Depends(get_database)
):
    """
    Accept parsed roles and save them into DB
    """
    result = confirm_orgchart(data["roles"], db)
    return {"status": "success", "roles": result}