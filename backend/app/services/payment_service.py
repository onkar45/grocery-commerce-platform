from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.order import Order
from app.models.inventory import Inventory
from app.models.order_item import OrderItem
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

def mark_payment_success(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise ValueError("Payment not found")

    order = db.query(Order).filter(Order.id == payment.order_id).first()

    # Deduct stock
    items = db.query(OrderItem).filter(
        OrderItem.order_id == order.id
    ).all()

    for item in items:
        inventory = db.query(Inventory).filter(
            Inventory.product_id == item.product_id
        ).with_for_update().first()

        inventory.stock_qty -= item.quantity
        inventory.reserved_qty -= item.quantity

    # Update order & payment
    order.status = "PAID"
    payment.status = "SUCCESS"
    payment.transaction_id = str(uuid.uuid4())

    db.commit()
    return payment


def mark_payment_failed(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise ValueError("Payment not found")

    order = db.query(Order).filter(Order.id == payment.order_id).first()

    # Release reserved stock
    items = db.query(OrderItem).filter(
        OrderItem.order_id == order.id
    ).all()

    for item in items:
        inventory = db.query(Inventory).filter(
            Inventory.product_id == item.product_id
        ).with_for_update().first()

        inventory.reserved_qty -= item.quantity

    order.status = "FAILED"
    payment.status = "FAILED"

    db.commit()
    return payment