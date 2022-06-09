# --- This module is used to encrypt the users password when they create an account or update their password.

# --- Import the required modules:
from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

# --- Set the encryption type for the passwords to use bcrypt:
def hash_pwd(password: str):
    """This function will take the password the user passed and create a hash oit and return it back hashed.
    Required parameter / argument: password: string.
    """
    return pwd_context.hash(password)


def verify_password_hash(plain_password:str, hashed_password:str):
    """
    Overview: 
        This function will verify the password that the user sends when they 
        login matches the password stored in the users table for that user.
    
    Args:
        plain_password (string): This is the password the user entered when they sent the login request.
        hashed_password (string): This is the hashed password that is stored in the database.

    Returns:
        Boolean: True if hashed passwords match, otherwise False.
    """
    # --- Verify that the passwords match and return true if so or false if not:
    return pwd_context.verify(plain_password, hashed_password)