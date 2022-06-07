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