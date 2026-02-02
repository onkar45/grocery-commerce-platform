from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.order import OrderCreateRequest, OrderResponse
from app.services.order_service import create_order
from app.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def place_order(
    data: OrderCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        order = create_order(db, user["user_id"], data.items)
        return {
            "order_id": order.id,
            "status": order.status,
            "total_amount": order.total_amount
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
