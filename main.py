from fastapi import FastAPI
from routers import function

app = FastAPI()

app.include_router(function.router, prefix="/api", tags=["Items"])

@app.get("/")
def root():
    return {"message": "This is the main app!"}