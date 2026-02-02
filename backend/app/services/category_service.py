from sqlalchemy.orm import Session
from app.models.category import Category

def create_category(db: Session, name: str, parent_id: int = None):
    # Convert 0 to None for root categories
    if parent_id == 0:
        parent_id = None
        
    category = Category(name=name, parent_id=parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
