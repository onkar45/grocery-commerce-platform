from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.payment import PaymentInitRequest, PaymentResponse
from app.services.payment_service import (
    initiate_payment,
    mark_payment_success,
    mark_payment_failed
)
from app.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/initiate", response_model=PaymentResponse)
def initiate(
    data: PaymentInitRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        payment = initiate_payment(db, data.order_id)
        return {
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "status": payment.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/success/{payment_id}")
def payment_success(payment_id: int, db: Session = Depends(get_db)):
    mark_payment_success(db, payment_id)
    return {"message": "Payment successful"}


@router.post("/failed/{payment_id}")
def payment_failed(payment_id: int, db: Session = Depends(get_db)):
    mark_payment_failed(db, payment_id)
    return {"message": "Payment failed"}
