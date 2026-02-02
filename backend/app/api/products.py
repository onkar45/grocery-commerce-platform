from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import create_product
from app.core.dependencies import get_db, require_permission

router = APIRouter(prefix="/products", tags=["Products"])

@router.post(
    "/",
    response_model=ProductResponse,
    dependencies=[Depends(require_permission("product:create"))]
)
def add_product(data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, data)
