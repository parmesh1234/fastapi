from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status

from ..models import Todos
from ..database import  SessionLocal
from ..routers.auth import get_current_user


router = APIRouter(
    prefix='/todos',
    tags=["todos"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]
class TodoRequest(BaseModel):
    title: str = Field(min_length=10, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool



@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Autheication Failed")

    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int= Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_models = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_models is not None:
        return todo_models
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,
                      db:db_dependency,
                      todo_request:TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_models = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_models)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency, db:db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_models = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_models is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_models.title = todo_request.title
    todo_models.description = todo_request.description
    todo_models.priority = todo_request.priority
    todo_models.complete = todo_request.complete

    db.add(todo_models)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db:db_dependency, todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticaiton failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).delete()
    db.commit()