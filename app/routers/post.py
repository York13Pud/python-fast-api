# --- Import the required modules:
from app.models import models
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.schemas import PostCreate, PostResponse, AllPostsResponseVotes
from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.param_functions import Query
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session


# --- Create a router variable that uses the APIRouter class:
router = APIRouter(
    # --- prefix will prefix /post to every route in this file. That way you don't
    # --- need to use /post on every rout / path operation:
    prefix = "/post",
    tags = ["Posts"]
    )


# --- Get all posts:
@router.get("/", 
            name = "Get All Posts.", 
            summary = "Returns the full list of available blog posts.", 
            response_model = List[AllPostsResponseVotes]
            )

def get_all_posts(db: Session = Depends(get_db),
                  limit: int = 10,
                  skip: int = 0,
                  search: Optional[str] = ""
                  ):
    
    # --- Get all the posts from the table.
    # --- 
    # --- Note: if you remove .all(), the result will be the actual SQL query that SQLAlchemy translates the ORM request to:
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
                       .join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True)\
                       .group_by(models.Post.id)\
                       .filter(models.Post.title.contains(search))\
                       .limit(limit = limit)\
                       .offset(offset = skip)\
                       .all()
    
    return results


# --- Get all my posts:
@router.get("/my-posts", 
            name = "Get All My Posts.",
            summary = "Returns the full list of available blog posts that the logged in user created.", 
            response_model = List[PostResponse]
            )

def get_my_posts(db: Session = Depends(get_db), 
                  current_user: int = Depends(get_current_user)
                  ):
    # --- Get all the posts from the table.
    # --- Note: if you remove .all(), the result will be the actual SQL query that SQLAlchemy translates the ORM request to:
    posts = db.query(models.Post)\
           .filter(models.Post.owner_id == current_user.id)\
           .all()
        
    return posts


# --- Get one post record based on its id (path parameter):
@router.get("/{id}",
            name = "Get A Single Posts.", 
            summary = "Returns the details of a single blog posts.", 
            response_model = AllPostsResponseVotes
            )

def get_one_post(id: int = Query(..., description = "The ID number of the post you wish to return.", title="Post ID"),
                 db: Session = Depends(get_db)
                 ):
    
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    result = db.query(models.Post, func.count(models.Vote.post_id)\
             .label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True)\
             .group_by(models.Post.id).where(models.Post.id == id)\
             .first()
    
    
    if result == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found"
                            )
    
    return result


# --- Create a post:
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = PostResponse)
def new_post(post: PostCreate, 
             db: Session = Depends(get_db), 
             current_user: int = Depends(get_current_user)
             ):
    
    print(f"Current User ID: {current_user.id}")
    
    new_post = models.Post(owner_id = current_user.id, **post.dict() )
    
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(get_current_user)
                ):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    print(post.id)
    print(current_user.id)
    print(post.owner_id)
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")    
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        
    db.delete(post)
    db.commit()
                
    return Response(status_code = status.HTTP_200_OK)


# --- Update a post:   
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, 
                updated_post: PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(get_current_user)
                ):
    
    print(current_user.id)
                    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
        
    
    # --- If the post cannot be created, show an error:
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post {id} not found.")   
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    print(updated_post.dict())
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    # --- Return the value of the post:
    return post_query.first()