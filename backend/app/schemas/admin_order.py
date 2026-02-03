from pydantic import BaseModel
from datetime import datetime

class AdminOrderResponse(BaseModel):
    id: int 
    user_id: int
    status: str
    total_amount: float
    created_at: datetime

    class config:
        orm_mode = True