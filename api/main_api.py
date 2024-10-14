from fastapi import FastAPI, HTTPException
from .routers import content

app = FastAPI()
app.include_router(content.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
