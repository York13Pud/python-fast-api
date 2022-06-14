# --- Import the required modules:
from pydantic import BaseSettings


# --- Create a class to store all of the required environment variables into an object:
class Settings(BaseSettings):
    """This class will pull all of the environment variables listed below, type check them with pydantic and create an object."""
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

# --- Create a variable that calls the Settings class to return an object with all of the required settings:    
settings = Settings()