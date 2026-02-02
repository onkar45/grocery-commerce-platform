from sqlalchemy.orm import Session
from app.models.inventory import Inventory

def create_inventory(db: Session, product_id: int, stock_qty: int, reorder_level: int):
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

def update_stock(db: Session, product_id: int, stock_qty: int):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    inventory.stock_qty = stock_qty
    db.commit()
    db.refresh(inventory)
    return inventory
