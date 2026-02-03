from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.order import Order
from app.models.inventory import Inventory
from app.models.order_item import OrderItem
from app.services.audit_service import log_action
import uuid

def initiate_payment(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")

    if order.status != "CREATED":
        raise ValueError("Payment already processed")

    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        status="INITIATED"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def mark_payment_success(
    db: Session,
    payment_id: int,
    actor_id: int
):
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise ValueError("Payment not found")

        if payment.status == "SUCCESS":
            raise ValueError("Payment already successful")

        order = db.query(Order).filter(Order.id == payment.order_id).first()

        if order.status != "CREATED":
            raise ValueError("Invalid order state for payment success")

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:
            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).with_for_update().first()

            if inventory.reserved_qty < item.quantity:
                raise ValueError("Invalid reserved stock state")

            if inventory.stock_qty < item.quantity:
                raise ValueError("Insufficient stock")

            inventory.stock_qty -= item.quantity
            inventory.reserved_qty -= item.quantity

        order.status = "PAID"
        payment.status = "SUCCESS"
        payment.transaction_id = str(uuid.uuid4())

        db.commit()
        db.refresh(payment)

        log_action(
            db=db,
            actor_id=actor_id,
            action="PAYMENT_SUCCESS",
            resource="PAYMENT",
            resource_id=payment.id,
            message=f"Payment successful for order {order.id}"
        )

        return payment

    except Exception:
        db.rollback()
        raise


def mark_payment_failed(
    db: Session,
    payment_id: int,
    actor_id: int
):
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise ValueError("Payment not found")

        if payment.status == "FAILED":
            raise ValueError("Payment already failed")

        order = db.query(Order).filter(Order.id == payment.order_id).first()

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:
            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).with_for_update().first()

            if inventory.reserved_qty < item.quantity:
                raise ValueError("Invalid reserved stock state")

            inventory.reserved_qty -= item.quantity

        order.status = "FAILED"
        payment.status = "FAILED"

        db.commit()
        db.refresh(payment)

        log_action(
            db=db,
            actor_id=actor_id,
            action="PAYMENT_FAILED",
            resource="PAYMENT",
            resource_id=payment.id,
            message=f"Payment failed for order {order.id}"
        )

        return payment

    except Exception:
        db.rollback()
        raise
