from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.payment import Payment
from app.models.refund import Refund
from app.models.order_item import OrderItem
from app.models.inventory import Inventory

def cancel_order(db: Session, order_id: int, reason: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")

    if order.status == "SHIPPED" or order.status == "DELIVERED":
        raise ValueError("Order cannot be cancelled at this stage")

    # Case 1: Order not paid yet
    if order.status == "CREATED":
        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:
            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).with_for_update().first()

            inventory.reserved_qty -= item.quantity

        order.status = "CANCELLED"
        db.commit()
        return "Order cancelled successfully"

    # Case 2: Paid order → refund
    if order.status == "PAID":
        payment = db.query(Payment).filter(
            Payment.order_id == order.id,
            Payment.status == "SUCCESS"
        ).first()

        if not payment:
            raise ValueError("Payment not found")

        refund = Refund(
            payment_id=payment.id,
            amount=payment.amount,
            reason=reason,
            status="SUCCESS"
        )
        db.add(refund)

        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in items:
            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).with_for_update().first()

            inventory.stock_qty += item.quantity

        order.status = "REFUNDED"
        db.commit()
        return "Order cancelled and refunded"
