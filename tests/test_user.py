from fastapi.testclient import TestClient
from fastapi import status
from app.database import Base, get_db
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Setup test database
# toggle word wrap alt + z
SQL_ALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:rGo*Y6H_EPX_tReMp8PyMHAXKt76C@localhost:5432/fastapi_test'
# SQL_ALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

print(SQL_ALCHEMY_DATABASE_URL)

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency
# In every path operatio nwe need to pass a session
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



def test_root():
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello World"


def test_create_user():
    res = client.post("/users/", json={"email": "test@testmail.com", "password": "testpw123"})
    # don't forget to unpack the dict **
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@testmail.com"
    assert res.status_code == status.HTTP_201_CREATED