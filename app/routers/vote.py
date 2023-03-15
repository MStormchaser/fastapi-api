from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy import delete
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
                    prefix="/vote",
                    tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Check if posts exists so users can't vote on
    # non existing posts
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {vote.post_id} does not exist.")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    # dir == 1 upvote - dir == 0 downvote
    if vote.dir == 1:
        if found_vote:
             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user with ID {current_user.id} already voted on post with ID {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id )
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}