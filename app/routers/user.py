# --- Import the required modules:
from app import models
from app.auth.hash_pwd import hash_pwd
from app.database import get_db
from app.schemas import UserCreate, UserCreateResponse, UserDetailsResponse
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


# --- Create a router variable that uses the APIRouter class:
router = APIRouter()


# --- Create a user:
@router.post("/users", status_code = status.HTTP_201_CREATED, response_model = UserCreateResponse)
def new_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # --- Hash the users password:
    user.password = hash_pwd(user.password)

    # --- Define a variable to create a user object / model:
    new_user = models.User( **user.dict() )
    
    try:
        # --- Add the post to the table. You must use commit to write the post tot the table:
        db.add(new_user)
        db.commit()
        
        # --- Use refresh to update new_post with the details of the newly written post:
        db.refresh(new_user)
    
    except Exception as error:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = f"The email address {user.email} already exists. Please try again with a different email address.")  
    
    # --- Return the value of the post:
    return new_user

@router.get("/users/{id}", response_model=UserDetailsResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"User ID {id} not found")
    
    return user