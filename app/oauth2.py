from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
import fastapi
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

# for the dependency get current user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY
# Algorythm
# Expiration Time

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # make a copy to not override user data
    to_encode = data.copy()
    # create expire time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # extend the user data dict with the expire information
    to_encode.update({"exp": expire})
    # create the jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the data from what we passed in the token
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        # verify it matches our schema
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exeption)

    user = db.query(models.User).filter(models.User.id == int(token.id)).first()

    return user

