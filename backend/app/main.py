from fastapi import FastAPI

app = FastAPI(title= "Enterprise Grocery Platform API")

@app.get('/')
def health():
    return{"status": "Ok"}