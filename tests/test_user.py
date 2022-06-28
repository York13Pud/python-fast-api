# --- Import the required modules:
from app.schemas import UserCreateResponse, Token
from app.config import settings
from jose import jwt
from pytest import mark


email = "sam@sam.sam"
password = "password123454648945456sddsfdffhgh4"
    
    
# --- Define a function that will test the root url of the app:
def test_user_create(fastapi_client):
    # --- Make a post request to the user URL to create a user:
    res = fastapi_client.post("/user/", 
                      json={"email": email, 
                            "password": password
                            })
    
    new_user = UserCreateResponse(**res.json())
    
    assert new_user.email == "sam@sam.sam"
    assert res.status_code == 201


# --- Define a function that will test the user login URL:
def test_user_login(fastapi_client, test_user):
    res = fastapi_client.post("/login", 
                    data={"username": test_user["email"], 
                        "password": test_user["password"]
                        })
    
    login_res = Token(**res.json())
    
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    


# --- Define a function that will test a failed user login URL:
@mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", None, 422),
    (None, "password123", 422)
])

def test_login_failure(test_user, fastapi_client, email, password, status_code):
    res = fastapi_client.post("/login", 
                    data={"username": email, 
                        "password": password
                        })
    
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials. Please Try Again."