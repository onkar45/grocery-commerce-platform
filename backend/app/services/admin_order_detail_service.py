from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment

def get_order_detail(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    items = db.query(OrderItem).filter(
        OrderItem.order_id == order.id
    ).all()

    payment = db.query(Payment).filter(
        Payment.order_id == order.id
    ).first()

    return {
        "order_id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "items": items,
        "payment": payment
    }
