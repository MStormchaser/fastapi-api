import psycopg
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from .config import settings

#1 Create URL
#2 Create Engine
#3 Create Session
#4 Connect to Base Class

# URL Structure: 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQL_ALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
# In every path operatio we need to pass a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This code is needed if we want to use raw sql instead of sqlalchemy
while True:
    try:
        conn = psycopg.connect(conninfo=f"host={settings.database_hostname} dbname={settings.database_name} user={settings.database_username} password={settings.database_password}")
        cur = conn.cursor()
        print("DB connection established")
        break
    except Exception as Error:
        print("DB error", Error)
        time.sleep(2)
