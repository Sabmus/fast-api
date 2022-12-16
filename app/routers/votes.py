from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from .. import database
from .. import models
from .. import oauth2


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteBase, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_active_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exists")

    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    vote_db = vote_query.first()

    # if true: like (or vote)
    if vote.post_dir:
        if vote_db is None:
            new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message": "succesfully vote a post!"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already vote that post title (#{vote.post_id})")
    
    # if false: unlike (downvote)
    if not vote.post_dir:
        if vote_db is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Can't downvote that post title (#{vote.post_id})")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "succesfully downvote a post!"}
