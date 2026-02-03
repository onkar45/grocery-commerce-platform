from pydantic import BaseModel

class RefundRequest(BaseModel):
    order_id: int
    reason: str
