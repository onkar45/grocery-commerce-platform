from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_permission
from app.services.admin_dashboard_service import get_dashboard_stats

router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Admin Dashboard"]
)

@router.get(
    "/stats",
    dependencies=[Depends(require_permission("admin_access"))]
)
def dashboard_stats(db: Session = Depends(get_db)):
    return get_dashboard_stats(db)
