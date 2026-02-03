from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuditLogResponse(BaseModel):
    id: int
    actor_id: int
    action: str
    resource: str
    resource_id: Optional[int]
    message: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
