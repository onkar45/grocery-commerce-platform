from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.schemas.admin_order import AdminOrderResponse
from app.services.admin_order_service import list_orders
from app.core.dependencies import get_db, require_permission

router = APIRouter(
    prefix="/admin/orders",
    tags=["Admin Orders"],
    dependencies=[Depends(require_permission("order:read"))]
)

@router.get("/", response_model=List[AdminOrderResponse])
def get_orders(
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return list_orders(
        db,
        status,
        user_id,
        start_date,
        end_date,
        skip,
        limit
    )
