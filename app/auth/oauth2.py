# --- Import the required modules / libraries:
from app import schemas
from app.config import settings
from app.database import get_db
from app.models.models import User
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")


# --- Three parts are needed:
# --- The SECRET_KEY can be created using the following terminal command:
# --- openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    # --- Make a copy of the data passed to the function:
    to_encode = data.copy()
    
    # --- Work out what the time will be in 30 minutes:
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # --- Add the expiration time to the to_encode variable:
    to_encode.update({"exp": expire})
    
    # --- Create the encoded JWT token:
    encoded_token = jwt.encode(claims = to_encode, 
                               key = SECRET_KEY, 
                               algorithm = ALGORITHM
                               )
    
    # --- Return the token:
    return encoded_token


def verify_access_token(token: str, credentials_exception):
    try: 
        # --- Decode the key
        payload = jwt.decode(token = token, 
                            key = SECRET_KEY, 
                            algorithms = ALGORITHM
                            )
        
        # --- Get the user_id that is part of the payload body:
        user_id: str = payload.get("user_id")

        # --- If the user_id is null, error:
        if id is None:
            raise credentials_exception
        
        # --- If the user_id is a number, set token_data to the user_id
        token_data = schemas.TokenData(id = user_id)

    # --- If a JWT related error occurs, raise an error using the credentials_exception variable:
    except JWTError:
        raise credentials_exception
    
    # --- Return the token data
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)): 
    # --- Define a variable that will be used to pass an error if the user is not authenticated:
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                          detail = "Invalid Credentials",
                                          headers = {"WWW-Authenticate": "Bearer"}
                                          )
    
    # --- Verify the access token:
    token = verify_access_token(token = token, 
                                credentials_exception = credentials_exception
                                )
    user = db.query(User).filter(User.id == token.id).first()
    
    print(user)
    
    return user