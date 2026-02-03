from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    amount = Column(Float, nullable=False)
    reason = Column(String(255))
    status = Column(String(50), default="INITIATED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
