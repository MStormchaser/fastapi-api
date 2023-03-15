from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# Pydantic Base model
# Validates the Post Data coming form the Endpoint
# So the Frontend just can send any data it wants
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# add to the decorator the response model
# response_model=schemas.PostResponse
# It's important to set the config class
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    # we need to import datetime from datetiem
    created_at: datetime
    user_id: int
    owner: UserOut


    class Config:
        orm_mode = True


class PostOut(BaseModel):
    #reference the class above to retreive all fields
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)




    
    