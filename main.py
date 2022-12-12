from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


# schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default True value
    rating: Optional[int] = None  # optional field


@app.get("/")
async def root():
    return {"message": "Welcome to my world!"}


@app.get("/posts")
def get_posts():
    return {"message": "this is a dummy data"}


@app.post("/posts")
def create_post(post: Post):
    """Create a post

    Args:
        post (Post): validated by FastApi based on Post Class

    Returns:
        _type_: _description_
    """
    print(post)  # pydantic object
    print(post.dict())  # regular python dict
    return {"post": {
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "rating": post.rating
    }}
