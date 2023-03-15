from fastapi import FastAPI
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

##### We only need this command below if we don't use alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# TEST in Browser Dev Tools - You need to be on a website in the origins list
# type ("in console
# fetch("http://localhost:8000/").then(res => res.json()).then(console.log)
origins = [
    "http://localhost.tiangolo.com",
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
