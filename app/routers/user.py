# --- Import the required modules:
from app.models import models
from app.auth.hash_pwd import hash_pwd
from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.schemas import UserCreate, UserCreateResponse, UserDetailsResponse
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


# --- Create a router variable that uses the APIRouter class:
router = APIRouter(
    # --- prefix will prefix /user to every route in this file. That way you don't
    # --- need to use /user on every rout / path operation:
    prefix = "/user",
    tags = ["User"]
    )


# --- Create a user:
@router.post("/", status_code = status.HTTP_201_CREATED, 
             response_model = UserCreateResponse)

def new_user(user: UserCreate, 
             db: Session = Depends(get_db)):
    
    # --- Hash the users password:
    user.password = hash_pwd(user.password)

    # --- Define a variable to create a user object / model:
    new_user = models.User( **user.dict() )

    # --- Add the post to the table. You must use commit to write the post tot the table:
    db.add(new_user)
    db.commit()
    
    # --- Use refresh to update new_post with the details of the newly written post:
    db.refresh(new_user)

    # --- Return the value of the post:
    return new_user


@router.get("/{id}", 
            response_model=UserDetailsResponse)

def get_user(id: int, 
             db: Session = Depends(get_db),
             current_user: int = Depends(get_current_user)):

    print(current_user.email)
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"User ID {id} not found")
    
    return user