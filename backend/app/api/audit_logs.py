from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.audit_log import AuditLogResponse
from app.models.audit_log import AuditLog
from app.core.dependencies import get_db, require_permission

router = APIRouter(
    prefix="/admin/audit-logs",
    tags=["Audit Logs"],
    dependencies=[Depends(require_permission("audit:read"))]
)

@router.get("/", response_model=List[AuditLogResponse])
def list_logs(
    action: Optional[str] = Query(None),
    resource: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)

    if resource:
        query = query.filter(AuditLog.resource == resource)

    return query.order_by(AuditLog.created_at.desc()).limit(100).all()
