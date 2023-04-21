import pytest
from app import schemas
from jose import jwt
from app.config import settings
from fastapi import status

from tests.conftest import test_user

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

def test_root(client):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello World"


def test_create_user(client):
    res = client.post("/users/", json={"email": "test@testmail.com", "password": "testpw123"})
    # don't forget to unpack the dict **
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@testmail.com"
    assert res.status_code == status.HTTP_201_CREATED


def test_login(client, test_user):
    # We don't pass the information in the Json body but as form-data
    # therefore we have to use 'data' instead of 'json'
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_user = schemas.Token(**res.json())

    payload = jwt.decode(login_user.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    # Extract the data from what we passed in the token
    id: str = payload.get("user_id")
    assert test_user["id"] == id
    assert login_user.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK

@pytest.mark.parametrize("email, password", [
    ("test@testmail.com", "wrong_password"),
    ("wrong_email", "test1234#"),
    ("wrong_email", "wrong_password")])
def test_incorrect_login(client, email, password):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert res.json().get("detail") == "Invalid credentials"
