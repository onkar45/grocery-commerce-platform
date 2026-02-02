from sqlalchemy.orm import Session
from app.models.product import Product

def create_product(db: Session, data):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
