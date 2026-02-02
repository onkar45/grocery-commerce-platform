from pydantic import BaseModel
from typing import List

class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int

class OrderCreateRequest(BaseModel):
    items: List[OrderItemRequest]

class OrderResponse(BaseModel):
    order_id: int
    status: str
    total_amount: float
