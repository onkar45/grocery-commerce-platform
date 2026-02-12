from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

from app.services.product_service import (
    get_products as get_products_service,
    create_product,
    update_product,
    delete_product
)

from app.core.dependencies import get_db, require_permission, get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


# ================================
# CREATE PRODUCT
# ================================
@router.post(
    "/",
    response_model=ProductResponse,
    dependencies=[Depends(require_permission("product:create"))]
)
def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_product(db, data, user["user_id"])


# ================================
# GET PRODUCTS (FILTER + SEARCH + PAGINATION)
# ================================
@router.get(
    "/",
    dependencies=[Depends(require_permission("product:read"))]
)
def get_products(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
):
    return get_products_service(db, category_id, search, page, limit)


# ================================
# UPDATE PRODUCT
# ================================
@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    dependencies=[Depends(require_permission("product:update"))]
)
def edit_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    try:
        return update_product(db, product_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ================================
# DELETE PRODUCT
# ================================
@router.delete(
    "/{product_id}",
    dependencies=[Depends(require_permission("product:delete"))]
)
def remove_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return delete_product(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
