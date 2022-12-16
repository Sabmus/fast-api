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


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db)):
    active_users = db.query(models.User).filter(models.User.active == True).all()  # try to get all user_ids in this query
    user_ids = [user.id for user in active_users]  # this should be deleted
    
    posts = db.query(models.Post).filter(models.Post.user_id.in_(user_ids)).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_active_user)):
    new_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve the newly created post
    return new_post


@router.get("/{id}", response_model=schemas.UserPosts)
def get_post(id: int, db: Session = Depends(database.get_db)):  # FastApi does the int conversion
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_active_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)  #.filter(models.Post.user_id==current_user.id)
    post_to_delete = post_query.first()

    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    elif post_to_delete.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have access to do this action")
    else:
        post_query.delete(synchronize_session=False)
        db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_active_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)  #.filter(models.Post.user_id==current_user.id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    elif post_to_update.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have access to do this action")
    else:
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
    
    return post_query.first()
