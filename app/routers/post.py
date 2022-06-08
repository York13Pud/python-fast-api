# --- Import the required modules:
from app import models
from app.database import get_db
from app.schemas import PostCreate, PostResponse
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session


# --- Create a router variable that uses the APIRouter class:
router = APIRouter()

# --- Get all posts:
@router.get("/posts", response_model = List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    # --- Get all the data from the table.
    # --- Note: if you remove .all(), the result will be the actual SQL query that SQLAlchemy translates the ORM request to:
    posts = db.query(models.Post).all()
        
    return posts


# --- Get one post record based on its id (path parameter):
@router.get("/posts/{id}", response_model = PostResponse)
def get_one_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")

    return post


# --- Create a post:
@router.post("/posts", status_code = status.HTTP_201_CREATED, response_model = PostResponse)
def new_post(post: PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post( **post.dict() )
    
    # --- Add the post to the table. You must use commit to write the post tot the table:
    db.add(new_post)
    db.commit()
    
    # --- Use refresh to update new_post with the details of the newly written post:
    db.refresh(new_post)
    
    # --- If the post cannot be created, show an error:
    if not new_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Post could not be created.")   
    
    # --- Return the value of the post:
    return new_post


# --- Delete a post:
@router.delete("/delete/{id}", response_model = PostResponse)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        db.delete(post)
        db.commit()
    
    except Exception as error:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")
            
    raise HTTPException(status_code = status.HTTP_200_OK,
                        detail = f"Post {id} has been deleted.")


# --- Update a post:   
@router.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    db.commit()
    
    # --- If the post cannot be created, show an error:
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post {id} not found.")   
    
    # --- Return the value of the post:
    return post