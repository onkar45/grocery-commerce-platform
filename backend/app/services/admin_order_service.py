from sqlalchemy.orm import Session
from app.models.order import Order
from datetime import datetime

def list_orders(
    db: Session,
    status: str = None,
    user_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    skip: int = 0,
    limit: int = 20
):
    query = db.query(Order)

    if status:
        query = query.filter(Order.status == status)
    
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    
    if end_date:
        query = query.filter(Order.created_at <= end_date)

    query = query.order_by(Order.created_at.desc())

    return query.offset(skip).limit(limit).all()