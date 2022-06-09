from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.oauth2 import create_access_token
from app.schemas import UserLogin
from app.auth.hash_pwd import verify_password_hash

router = APIRouter(tags = ["Authentication"])

@router.post("/login")
# --- Note: OAuth2PasswordRequestForm requires the credentials to be sent as a form rather than JSON body.
# --- It requires a "username" and a "password" to be sent in the form.
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # --- Query the database to find the user account by their email address:
    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    # --- If the user cannot be found, raise a 404:
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found. Please try again.")
    
    # --- Check the password entered by the user matches the hashed password in the users table for that user:
    check_hash = verify_password_hash(plain_password = user_credentials.password, hashed_password = user.password)
    
    # --- If check_has is false, raise a 404:
    if not check_hash:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid email address and / or password.")
    
    # --- If the users password matches, generate a JWT bearer token:
    access_token = create_access_token(data = {"user_id": user.id})
    
    # --- Return the token details to the user:
    return {"access_token": access_token,
            "token_type": "bearer"
            }