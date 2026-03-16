from sqlalchemy.orm import Session
from app.workspaces.models import Workspace

def add_workspace(db: Session, name:str, image:bytes, user_id:int):
    workspace = Workspace(name=name, image=image, user_id=user_id)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace

def get_workspace_by_user_id(db: Session, user_id: int):
    return db.query(Workspace).filter(Workspace.user_id == user_id).first()