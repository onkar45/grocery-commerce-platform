from sqlalchemy.orm import Session
from app.models.product import Product
from app.services.audit_service import log_action

def create_product(db, data, actor_id):
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