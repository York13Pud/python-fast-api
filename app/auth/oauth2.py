# --- Import the required modules / libraries:
from jose import JWTError, jwt
from datetime import datetime, timedelta

# --- Three parts are needed:
SECRET_KEY = "47e2ffb22ef6e8f134e5481228a2a3dd3c990a52e084bc399b616b576813254a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    # --- Make a copy of the data passed to the function:
    to_encode = data.copy()
    
    # --- Work out what the time will be in 30 minutes:
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # --- Add the expiration time to the to_encode variable:
    to_encode.update({"exp": expire})
    
    # --- Create the encoded JWT token:
    encoded_token = jwt.encode(claims = to_encode, 
                               key = SECRET_KEY, 
                               algorithm = ALGORITHM
                               )
    
    # --- Return the token:
    return encoded_token