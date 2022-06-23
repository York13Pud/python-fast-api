# --- Import the required modules:
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserCreateResponse


# --- Create the client to interact with the app:
client = TestClient(app)


# --- Define a function that will test the root url of the app:
def test_user_create():
    # --- Make a post request to the user URL to create a user:
    res = client.post("/user/", 
                      json={"email": "sam@sam.sam", 
                            "password": "password123454648945456sddsfdffhgh4"
                            })
    
    new_user = UserCreateResponse(**res.json())
    
    assert new_user.email == "sam@sam.sam"
    assert res.status_code == 201
    