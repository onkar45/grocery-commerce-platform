from fastapi import FastAPI
from app.api import auth

app = FastAPI(title="Enterprise Grocery Platform API")

app.include_router(auth.router)

@app.get("/")
def health():
    return {"status": "Auth system running"}
