import os
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor


load_dotenv()


app = FastAPI()


try:
    conn = psycopg2.connect(
        host = 'fast_api-postgres-1',
        database = os.getenv('POSTGRES_DB'),
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        cursor_factory = RealDictCursor
    )
    cursor = conn.cursor()
    print('db connection succesfully')
except psycopg2.OperationalError as error:
    print('db connection failed: OperatioanlError: ', error)
except psycopg2.DatabaseError as error:
    print('db connection failed: DatabaseError: ', error)


# schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default True value
    rating: Optional[int] = None  # optional field


my_posts = [
    {"title": "title of post 1", "content": "content of post 1, using docker", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None


@app.get("/")
async def root():
    return {"message": "Welcome to my world!"}


@app.get("/posts")
def get_posts():
    cursor.execute("select * from public.posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """Create a post

    Args:
        post (Post): validated by FastApi based on Post Class

    Returns:
        _type_: _description_
    """
    # print(post)  # pydantic object
    # print(post.dict())  # regular python dict
    
    cursor.execute("insert into public.posts (title, content, published, rating) values (%s, %s, %s, %s) returning *", 
                    (post.title, post.content, post.published, post.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):  # FastApi does the int conversion
    cursor.execute("select * from public.posts where id = %s", (str(id)))
    post = cursor.fetchone()

    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
        # the above is equal to below
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post {id} not found"}

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
    
