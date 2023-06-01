from fastapi import FastAPI, Depends
from .database.database import SessionLocal, engine
from .models import models
from .dependencies import get_query_token, get_token_header
from .routers import users, auth


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
