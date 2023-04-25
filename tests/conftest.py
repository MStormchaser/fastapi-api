#######################
#######################
#######################

# This file could contain all fixtures
# Fixtures that are in this file don't need to imported in this or subdirectories

#######################
#######################
#######################

from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.config import settings
import pytest
from fastapi import Depends, status
from app.oauth2 import create_access_token
from app import models
from app import database


# Setup test database _test
# toggle word wrap alt + z
SQL_ALCHEMY_DATABASE_URL_TEST = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQL_ALCHEMY_DATABASE_URL_TEST)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup Test Database Option 1
'''
This is one simple way of setting the client fixture. Howerver,
if we want access to our db object we need to to the following 
below...

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # drop old tables before test runs
    # deleting it before a new testrun instead of after each run
    # can help when troubleshooting your app
    Base.metadata.drop_all(bind=engine)
    # create new tables befor test runs
    Base.metadata.create_all(bind=engine)
    # create test client
    yield TestClient(app)
    '''

# Setup Test Database Option 2
@pytest.fixture(scope=("function"))
def session():
    # This gives us access to the session obj. 
    # just in case we need to query our db directly
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@testmail.com", "password": "test1234#"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == status.HTTP_201_CREATED
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture(scope="function")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


'''
@pytest.fixture
def test_posts(test_user, session):
      
    post_data = {"title": "First Post Title",
    "content": "First Post Content",
    "user_id": test_user["id"]}

    def create_post_model(post):
        return models.Post(**post)
    
    # posts_map = map(create_post_model, post_data)

    posts_list = dict(post_data)
    
    

    new_post = models.Post(posts_list)

    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post
'''

    


@pytest.fixture
def test_posts(test_user, session):
    post_data = {"title": "First Post Title",
        "content": "First Post Content",
        "user_id": "1"}
    
    post_data_long = [{"title": "First Post Title",
        "content": "First Post Content",
        "user_id": test_user["id"]},

        {"title": "2nd Post Title",
        "content": "2nd Post Content",
        "user_id": test_user["id"]},

        {"title": "3rd Post Title",
        "content": "3rd Post Content",
        "user_id": test_user["id"]}]
    

    query_str = """
                                    INSERT INTO posts (title, content, user_id)
                                    VALUES (%s, %s, %s) returning *"""
    
    query_vars = post_data["title"], post_data["content"], post_data["user_id"]

    new_post = database.cur.execute(query_str, query_vars)
    # need new cursor
    
    return new_post.fetchall()
