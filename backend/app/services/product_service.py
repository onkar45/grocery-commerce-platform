from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.product import Product
from app.models.category import Category
from app.services.audit_service import log_action

def list_products(db: Session):
    """Get all products with category information"""
    return db.query(Product).options(joinedload(Product.category)).all()

def get_products(
    db: Session,
    category_id: int | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 5
):
    query = db.query(Product).options(joinedload(Product.category))

    # 🔍 Category Filter
    if category_id:
        query = query.filter(Product.category_id == category_id)

    # 🔎 Search by name
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    total = query.count()

    products = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "category_id": p.category_id,
                "category_name": p.category.name if p.category else None
            }
            for p in products
        ]
    }

def create_product(db: Session, data, actor_id: int):
    """Create a new product"""
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)

    log_action(
        db=db,
        actor_id=actor_id,
        action="PRODUCT_CREATE",
        resource="PRODUCT",
        resource_id=product.id,
        message=f"Product created: {product.name}"
    )

    return product

def update_product(db: Session, product_id: int, data):
    """Update an existing product"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise ValueError("Product not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    """Delete a product"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise ValueError("Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
