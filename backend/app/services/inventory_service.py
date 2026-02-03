from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.services.audit_service import log_action

def create_inventory(
    db: Session,
    product_id: int,
    stock_qty: int,
    reorder_level: int
):
    inventory = Inventory(
        product_id=product_id,
        stock_qty=stock_qty,
        reserved_qty=0,
        reorder_level=reorder_level
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


def update_stock(
    db: Session,
    product_id: int,
    stock_qty: int,
    actor_id: int
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory:
        raise ValueError("Inventory not found for this product")

    if stock_qty < 0:
        raise ValueError("Stock quantity cannot be negative")

    old_qty = inventory.stock_qty
    inventory.stock_qty = stock_qty

    db.commit()
    db.refresh(inventory)

    log_action(
        db=db,
        actor_id=actor_id,
        action="INVENTORY_UPDATE",
        resource="PRODUCT",
        resource_id=product_id,
        message=f"{old_qty} → {stock_qty}"
    )

    return inventory
