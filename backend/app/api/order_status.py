from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.order_status import OrderStatusUpdate
from app.services.order_status_service import update_order_status
from app.core.dependencies import get_db, require_permission

router = APIRouter(prefix="/orders/status", tags=["Order Status"])

@router.put(
    "/{order_id}",
    dependencies=[Depends(require_permission("order:update"))]
)
def change_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    try:
        order = update_order_status(db, order_id, data.status)
        return {
            "order_id": order.id,
            "new_status": order.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
