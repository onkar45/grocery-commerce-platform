from sqlalchemy.orm import Session
from app.models.order import Order
from app.services.audit_service import log_action

ALLOWED_TRANSITIONS = {
    "PAID": ["PACKED"],
    "PACKED": ["SHIPPED"],
    "SHIPPED": ["DELIVERED"],
}

def update_order_status(
    db: Session,
    order_id: int,
    new_status: str,
    actor_id: int
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")

    old_status = order.status

    # ❗ Validate transition
    if old_status not in ALLOWED_TRANSITIONS:
        raise ValueError("Order status cannot be changed")

    if new_status not in ALLOWED_TRANSITIONS[old_status]:
        raise ValueError(
            f"Invalid transition from {old_status} to {new_status}"
        )

    # ✅ Update status
    order.status = new_status
    db.commit()
    db.refresh(order)

    # ✅ Audit log
    log_action(
        db=db,
        actor_id=actor_id,
        action="ORDER_STATUS_UPDATE",
        resource="ORDER",
        resource_id=order.id,
        message=f"{old_status} → {new_status}"
    )

    return order
