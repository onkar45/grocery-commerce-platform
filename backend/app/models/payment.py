from sqlalchemy import Column, String, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key = True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable= False)
    status = Column(String(50), default = "INITIATED")
    transaction_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default = func.now())
    