from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database
from .. import schemas
from .. import models
from .. import utils
from .. import oauth2


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm has username as field, so "email" would be saved inside "username"
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
