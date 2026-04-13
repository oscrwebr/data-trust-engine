from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

class Folder(BaseModel):
    graph_id: str
    name: str
    web_url: str
    parent_graph_id: str

class File(BaseModel):
    graph_id: str
    name: str
    extension: str
    hash: str | None=None
    hash_type: str | None=None
    last_scanned: datetime | None=None
    last_modified: datetime
    web_url: str
    parent_graph_id: str