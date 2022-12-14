from fastapi import FastAPI
from dotenv import load_dotenv

from .database import engine
from . import models
from .routers import posts, users


# for loading env file
load_dotenv()
# check if tables exists, else creates it
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my world!"}
