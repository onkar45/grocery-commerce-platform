from sqlalchemy.orm import Session
from app.models.order import Order

ALLOWED_TRANSITIONS = {
    "PAID": ["PACKED"],
    "PACKED": ["SHIPPED"],
    "SHIPPED": ["DELIVERED"],
}

def update_order_status(db: Session, order_id: int, new_status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")

    current = order.status

    if current not in ALLOWED_TRANSITIONS:
        raise ValueError("Order status cannot be changed")

    if new_status not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(
            f"Invalid transition from {current} to {new_status}"
        )

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
