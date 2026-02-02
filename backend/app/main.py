from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Enterprise Grocery Platform API")


@app.on_event("startup")
def create_tables():
    # Import models here to ensure they're registered with Base
    from app.models import user, role, permission, role_permission,user_role
    Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    try:
        engine.connect()
        return {"status": "DB connected"}
    except Exception as e:
        return {"status": "DB error", "error": str(e)}
