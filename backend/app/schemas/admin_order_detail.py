from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemDetail(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True

class PaymentDetail(BaseModel):
    id: int
    status: str
    amount: float
    transaction_id: Optional[str]

    class Config:
        orm_mode = True

class AdminOrderDetailResponse(BaseModel):
    order_id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemDetail]
    payment: Optional[PaymentDetail]
