from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import create_category
from app.core.dependencies import get_db, require_permission
from app.models.category import Category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post(
    "/",
    response_model=CategoryResponse,
    dependencies=[Depends(require_permission("product:create"))]
)
def add_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, data.name, data.parent_id)

@router.get("/", response_model=list[CategoryResponse])   # ✅ Add response model
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
