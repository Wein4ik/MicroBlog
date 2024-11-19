from fastapi import FastAPI, HTTPException
from api.routers import content, user

app = FastAPI()
app.include_router(content.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
