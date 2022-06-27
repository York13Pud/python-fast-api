# --- Import the required modules:
from app.config import settings
from app.schemas import UserCreateResponse
from app.database import get_db, Base
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# --- Create a constant that will be used to point to and pass the user details to our database:
SQLALCHEMY_DATABASE_URL = f"{settings.database_type}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


# --- Create an engine to connect to the database:
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# --- Create a session to the database:
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Execute the connection to the database and close it when finished:
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- This will override the get_db variable with the override_get_db to use a testing DB instead.
app.dependency_overrides[get_db] = override_get_db


# --- Create the tables in the test database:
Base.metadata.create_all(bind = engine)


@pytest.fixture
def client():
    
    yield TestClient(app)
    
    
# --- Define a function that will test the root url of the app:
def test_user_create(client):
    # --- Make a post request to the user URL to create a user:
    res = client.post("/user/", 
                      json={"email": "sam@sam.sam", 
                            "password": "password123454648945456sddsfdffhgh4"
                            })
    
    new_user = UserCreateResponse(**res.json())
    
    assert new_user.email == "sam@sam.sam"
    assert res.status_code == 201
    