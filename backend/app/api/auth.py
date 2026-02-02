from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token
from app.core.dependencies import get_db
from app.services.rbac_service import get_user_roles, get_user_permissions
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = create_user(db, data.email, data.password)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: Optional[str] = Form(None),
    scope: str = Form(""),
    client_id: Optional[str] = Form(None),
    client_secret: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login for Swagger UI.
    Manually handle form fields to avoid OAuth2PasswordRequestForm issues.
    """
    try:
        print(f"Login attempt - Username: {username}")
        print(f"Grant type: {grant_type}")
        print(f"Scope: {scope}")
        
        # Use username as email
        user = authenticate_user(db, username, password)
        if not user:
            print(f"Authentication failed for user: {username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print(f"Authentication successful for user: {username}")
        
        roles = get_user_roles(db, user.id)
        permissions = get_user_permissions(db, user.id)

        print(f"User roles: {[r.name for r in roles]}")
        print(f"User permissions: {[p[0] for p in permissions]}")

        token = create_access_token({
            "user_id": user.id,
            "roles": [r.name for r in roles],
            "permissions": [p[0] for p in permissions]
        })

        return {"access_token": token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        print(f"Error type: {type(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login-json", response_model=TokenResponse)
def login_json(data: LoginRequest, db: Session = Depends(get_db)):
    """
    JSON login endpoint for direct API calls (like Postman).
    """
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    roles = get_user_roles(db, user.id)
    permissions = get_user_permissions(db, user.id)

    token = create_access_token({
        "user_id": user.id,
        "roles": [r.name for r in roles],
        "permissions": [p[0] for p in permissions]
    })

    return {"access_token": token, "token_type": "bearer"}