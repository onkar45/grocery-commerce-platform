from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.user import User

def create_order(db: Session, user_id: int, items):
    total_amount = 0

    # 1️⃣ Check stock availability
    for item in items:
        inventory = db.query(Inventory).filter(
            Inventory.product_id == item.product_id
        ).with_for_update().first()

        if not inventory:
            raise ValueError("Inventory not found")

        available = inventory.stock_qty - inventory.reserved_qty
        if available < item.quantity:
            raise ValueError(f"Insufficient stock for product {item.product_id}")

    # 2️⃣ Reserve stock
    for item in items:
        inventory = db.query(Inventory).filter(
            Inventory.product_id == item.product_id
        ).with_for_update().first()

        inventory.reserved_qty += item.quantity

    # 3️⃣ Create order
    order = Order(
        user_id=user_id,
        status="CREATED",
        total_amount=0
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # 4️⃣ Create order items
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        price = product.price * item.quantity
        total_amount += price

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)

    # 5️⃣ Update total amount
    order.total_amount = total_amount
    db.commit()
    db.refresh(order)

    return order


def get_all_orders(db):
    return (
        db.query(
            Order.id,
            Order.total_amount,
            Order.status,
            User.email.label("user_email")
        )
        .join(User, User.id == Order.user_id)
        .all()
    )

def update_status_and_inventory(db: Session, order_id: int, status: str):
    print("🔥 FORCED INVENTORY UPDATE START 🔥")

    items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).all()

    print("ITEM COUNT:", len(items))

    for item in items:
        inventory = db.query(Inventory).filter(
            Inventory.product_id == item.product_id
        ).first()

        print("FOUND INVENTORY:", inventory.product_id)

        inventory.stock_qty = inventory.stock_qty - 1
        inventory.reserved_qty = 0

    db.commit()
    return {"message": "FORCED UPDATE"}

