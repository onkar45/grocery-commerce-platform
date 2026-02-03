from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, nullable=False)   # admin / staff user_id
    action = Column(String(100), nullable=False) # e.g. ORDER_STATUS_UPDATE
    resource = Column(String(100), nullable=False) # e.g. ORDER
    resource_id = Column(Integer, nullable=True)
    message = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
