from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import AdminCreateRequest, UserResponse
from app.services.admin_service import create_admin_user
from app.core.dependencies import get_db, require_permission

router = APIRouter(
    prefix="/admins",
    tags=["Admin Management"]
)

@router.post(
    "/",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("role:manage"))]
)
def create_admin(
    data: AdminCreateRequest,
    db: Session = Depends(get_db)
):
    try:
        user = create_admin_user(db, data.email, data.password, data.role)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
