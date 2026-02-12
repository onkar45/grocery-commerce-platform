from pydantic import BaseModel
from typing import List

class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int

class OrderCreateRequest(BaseModel):
    items: List[OrderItemRequest]

class OrderResponse(BaseModel):
    id: int
    user_email: str
    total_amount: float
    status: str

    class Config:
        from_attributes = True