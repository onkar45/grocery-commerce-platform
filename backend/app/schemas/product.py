from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductUpdate(BaseModel):
    name: str
    price: float
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    is_active: bool
    category_id: int
    category_name: Optional[str] = None 

    class Config:
        orm_mode = True
