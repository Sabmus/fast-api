from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from .. import models
from .. import utils


router = APIRouter(
    prefix="/users"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} is not found")
    
    return user
