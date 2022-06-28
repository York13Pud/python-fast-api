# --- Import the required modules:
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.models.models import Post, Vote
from app.schemas import Voting

from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.param_functions import Query
from typing import List, Optional
from sqlalchemy.orm import Session


# --- Create a router variable that uses the APIRouter class:
router = APIRouter(
    # --- prefix will prefix /vote to every route in this file. That way you don't
    # --- need to use /vote on every rout / path operation:
    prefix = "/vote",
    tags = ["Votes"]
    )

@router.post("/",            
             name = "Submit a like or Unlike for a post.", 
             summary = "Creates / removes an entry in the votes table to indicate if a post is liked or note",
             status_code = status.HTTP_201_CREATED)

def vote(vote: Voting, 
         db: Session = Depends(get_db), 
         current_user: int = Depends(get_current_user)):
    
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post does not exist.")
    
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
                                detail = f"User has already voted on post {vote.post_id}.")
        new_vote = Vote(post_id = vote.post_id, 
                        user_id = current_user.id)
        
        db.add(new_vote)
        db.commit()
        return {"detail": "vote added successfully."}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "vote does not exist.")
        
        vote_query.delete(synchronize_session = False)
        db.commit()
        
        return {"detail": "vote removed successfully."}