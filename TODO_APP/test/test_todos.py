from .utils import *
from ..main import app
from ..routers.todos import  get_db, get_current_user
from fastapi import status
from ..models import Todos


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title":"Learn to code",
        "description" :"need to learn everyday",
        "priority":5,
        "complete" : False,
        "owner_id" : 1,
        "id":1
    }]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title":"Learn to code",
        "description" :"need to learn everyday",
        "priority":5,
        "complete" : False,
        "owner_id" : 1,
        "id":1
    }


def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail" : "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "new todo to be created",
        "description": "new todo description",
        "priority": 4,
        "complete": False,
    }

    response = client.post("/todos", json=request_data)
    assert response.status_code ==  201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "title":"Learn to code from python",
        "description" :"need to learn everyday",
        "priority":5,
        "complete" : False,

    }

    response = client.put("/todos/1" ,json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model  = db.query(Todos).filter(Todos.id ==1).first()
    assert model.title == "Learn to code from python"


def test_update_todo_not_found(test_todo):
    request_data = {
        "title":"Learn to code from python",
        "description" :"need to learn everyday",
        "priority":5,
        "complete" : False,

    }

    response = client.put("/todos/999" ,json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail":"Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todos/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail" :"Todo not found"}
