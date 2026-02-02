from pydantic import BaseModel

class InventoryCreate(BaseModel):
    product_id: int
    stock_qty: int
    reorder_level: int = 5

class InventoryResponse(BaseModel):
    product_id: int
    stock_qty: int
    reserved_qty: int
    reorder_level: int

    class Config:
        orm_mode = True
