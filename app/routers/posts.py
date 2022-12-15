from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from typing import List

from .. import database
from .. import schemas
from .. import models
from .. import oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_active_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve the newly created post
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(database.get_db)):  # FastApi does the int conversion
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_active_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    else:
        post_query.delete(synchronize_session=False)
        db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_active_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    else:
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
    
    return post_query.first()
