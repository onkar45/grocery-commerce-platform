from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from typing import Optional

def log_action(
    db: Session,
    actor_id: int,
    action: str,
    resource: str,
    resource_id: Optional[int] = None,
    message: Optional[str] = None
):
    """
    Log an audit action to the database
    """
    audit_log = AuditLog(
        actor_id=actor_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        message=message
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    
    return audit_log

def get_audit_logs(
    db: Session,
    action: Optional[str] = None,
    resource: Optional[str] = None,
    limit: int = 100
):
    """
    Get audit logs with optional filtering
    """
    query = db.query(AuditLog)
    
    if action:
        query = query.filter(AuditLog.action == action)
    
    if resource:
        query = query.filter(AuditLog.resource == resource)
    
    return query.order_by(AuditLog.created_at.desc()).limit(limit).all()