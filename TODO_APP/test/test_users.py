from .utils  import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user


def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["username"] == "parmesh1042"


def test_change_password_success(test_user):
    response  = client.put("/users/change_pswd", json={"password":"test1234", "new_password":"test12345"})
    assert response.status_code == 204


def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/change_pswd", json={"password": "test1234s", "new_password": "test12345"})
    assert response.status_code == 401
    assert response.json() == {"detail":"Current Password is incorrect"}


def test_change_phone_number_success(test_user):
    response = client.put("/users/update_phone_number/9839393939")
    assert response.status_code == 204




