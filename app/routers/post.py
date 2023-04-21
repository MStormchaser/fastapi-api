
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import schemas, models, oauth2

from app import database

router = APIRouter(
                    prefix="/posts",
                    tags=["Posts"])


# The schema by default usuall checks the response against
# one post. If we try this we will get an error because we retrieve
# a list of posts. From typing we have to import list and than put
# the response model in a list.
# @router.get("/", response_model=list[schemas.PostOut])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    '''cur.execute("""SELECT * FROM posts """)
    posts = cur.fetchall()'''

    '''
    # GET all posts and votes
    select posts.*, count(votes.post_id) as votes from posts left join votes on votes.post_id = posts.id group by posts.id;
    '''

    # print(limit)
    posts_query = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    posts = posts_query.all()
    # We perform a left ourter join between Post on left and Votes on right
    # We count the occurance of post_id in the new table
    # For count() we have to import -> from sqlalchemy import func
    # Rename column .label()
    results_alchemy = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    results = database.cur.execute("select posts.*, count(votes.post_id) as votes from posts left join votes on votes.post_id = posts.id group by posts.id")
    field_name = [desc[0] for desc in database.cur.description]
    posts_named = [{field_name[i]: value[i] for i in range(len(field_name))} for value in results.fetchall()]
    # print(posts_named)

    return results_alchemy


# The id field is a path parameter
# The path parameter has to be convertet to INT
# id: int -> checks if convertable and converts to INT
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    '''cur.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id), ))
    my_post = cur.fetchone()
    '''
    my_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not my_post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with ID {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return my_post


# reference the Post Pydantic Model
# assign it to the variable payload
# the variable is a Pydantic Model that has a method .dict()
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    '''cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *
                """, (payload.title, payload.content, payload.published))
    new_post = cur.fetchone()
    conn.commit()'''

    # print(current_user.email)

    # payload in this case is a pydantic model
    # we can call the method .dict() on it
    # with ** we can upack the dict and put it in the same format as - title=payload.title, etc -
    # this is the most efficient way
    new_post = models.Post(user_id=current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    # Equal to the RETURNING statement in SQL
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    '''cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cur.fetchone()
    conn.commit()'''
    #lockup the value
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # validate it exists with .first() and check
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} found.")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user action")

    # delete & commit
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Here we want to use a schema
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    '''cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                (payload.title, payload.content, payload.published, str(id)) )
    updated_post = cur.fetchone()
    conn.commit()'''
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id {id} found.")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user action")


    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()