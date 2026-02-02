from fastapi import FastAPI
from app.api import auth, users,admins
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Enterprise Grocery Platform API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admins.router)

@app.on_event("startup")
def create_tables():
    # Import models here to ensure they're registered with Base
    from app.models import user, role, permission, user_role, role_permission
    Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "Auth system running"}
