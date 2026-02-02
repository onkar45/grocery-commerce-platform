from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.dependencies import get_db
from app.models.category import Category
from app.models.product import Product

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    categories = (
        db.query(Category)
        .filter(Category.is_active == True)
        .all()
    )

    return [
        {
            "id": c.id,
            "name": c.name,
            "parent_id": c.parent_id
        }
        for c in categories
    ]


@router.get("/products")
def list_products(
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.is_active == True)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    products = query.all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category_id": p.category_id
        }
        for p in products
    ]


@router.get("/products/{product_id}")
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.is_active == True
        )
        .first()
    )

    if not product:
        return {"error": "Product not found"}

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category_id": product.category_id
    }


