from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.refund import RefundRequest
from app.services.refund_service import cancel_order
from app.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/refunds", tags=["Refunds"])

@router.post("/cancel")
def cancel(
    data: RefundRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        message = cancel_order(db, data.order_id, data.reason)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
