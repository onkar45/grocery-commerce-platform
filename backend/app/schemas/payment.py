from pydantic import BaseModel

class PaymentInitRequest(BaseModel):
    order_id: int

class PaymentResponse(BaseModel):
    payment_id: int
    order_id: int
    status: str
