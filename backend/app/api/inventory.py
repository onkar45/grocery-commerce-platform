from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.inventory import InventoryCreate, InventoryResponse
from app.services.inventory_service import create_inventory, update_stock
from app.core.dependencies import get_db, require_permission

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post(
    "/",
    response_model=InventoryResponse,
    dependencies=[Depends(require_permission("product:update"))]
)
def add_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory(
        db,
        data.product_id,
        data.stock_qty,
        data.reorder_level
    )

@router.put(
    "/{product_id}",
    response_model=InventoryResponse,
    dependencies=[Depends(require_permission("product:update"))]
)
def update_inventory(
    product_id: int,
    stock_qty: int,
    db: Session = Depends(get_db)
):
    return update_stock(db, product_id, stock_qty)
