from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, APIRouter, Query
from starlette import status

from ..models import Todos, Users
from ..database import  SessionLocal
from ..routers.auth import get_current_user
from passlib.context import  CryptContext


router = APIRouter(
    prefix='/users',
    tags=['users']
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="User Not Authenticated")

    return db.query(Users).filter(Users.id == user.get("id")).all()


@router.put('/change_pswd', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency,user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="User Not Authenticated")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Current Password is incorrect")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put('/update_phone_number/{new_number}', status_code=status.HTTP_204_NO_CONTENT)
async def udpate_phone_number(user:user_dependency, db:db_dependency,new_number:str=Path(min_length=5)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not Authenticated")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    user_model.phone_number = new_number

    db.add(user_model)
    db.commit()
