# --- Import the required modules:
from app.models import models
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.schemas import PostCreate, PostResponse
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
             summary = "Creates / removes an entry in the votes table to indicat if a post is liked or note",
             status_code = status.HTTP_201_CREATED)
def vote():
    pass