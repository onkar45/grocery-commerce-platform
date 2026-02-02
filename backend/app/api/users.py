from fastapi import APIRouter, Depends
from app.core.dependencies import require_permission, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/debug")
def debug_token(user=Depends(get_current_user)):
    """Debug endpoint to see what's in your JWT token"""
    return {"token_payload": user}

@router.get("/")
def list_users(user=Depends(require_permission("read_users"))):
    return {"message": "Only permitted users can see this", "user": user}
