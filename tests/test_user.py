# --- Import the required modules:
from app.schemas import UserCreateResponse, Token
from app.config import settings
from jose import jwt


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
def test_login_failure(test_user, fastapi_client):
    res = fastapi_client.post("/login", 
                    data={"username": test_user["email"], 
                        "password": "fjhdjhlfhusdhfhsdh8384uhh3ghuef87w9ydsuhd8y"
                        })
    
    assert res.status_code == 403
    assert res.json().get("detail") == "Invalid Credentials. Please Try Again."