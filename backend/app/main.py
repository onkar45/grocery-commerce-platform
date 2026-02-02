from fastapi import FastAPI
from app.db.session import engine

app = FastAPI(title="Enterprise Grocery Platform API")

@app.get("/")
def health():
    try:
        engine.connect()
        return {"status": "DB connected"}
    except Exception as e:
        return {"status": "DB error", "error": str(e)}
