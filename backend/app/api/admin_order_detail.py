from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.admin_order_detail import AdminOrderDetailResponse
from app.services.admin_order_detail_service import get_order_detail
from app.core.dependencies import get_db, require_permission

router = APIRouter(
    prefix="/admin/orders",
    tags=["Admin Orders"],
    dependencies=[Depends(require_permission("order:read"))]
)

@router.get("/{order_id}", response_model=AdminOrderDetailResponse)
def order_detail(order_id: int, db: Session = Depends(get_db)):
    order = get_order_detail(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
