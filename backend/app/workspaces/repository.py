from sqlalchemy.orm import Session
from app.workspaces.models import Workspace

def add_workspace(db: Session, name:str, image:bytes):
    workspace = Workspace(name=name, image=image)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace