# --- Import the required modules:
from app.main import app
from fastapi.testclient import TestClient
import pytest


# --- Create the client to interact with the app:
client = TestClient(app)

# --- Make a call to the root URL:
res = client.get("/")

def test_root_status_code():
    """Status code must be: 200"""
    res_status_code = res.status_code
    expected_status_code = 200
    assert res_status_code == expected_status_code, \
           f"The returned status code is: {res_status_code}. It must be {expected_status_code}."

# --- Define a function that will test the root url of the app:
def test_root_greeting():
    """Greeting text must be: 
       This is not the endpoint you are looking for!"""
    
    # --- Test to see if the response matches what we expect:
    res_greeting = res.json().get("greeting")
    expected_greeting = "This is not the endpoint you are looking for!"
    
    assert res_greeting ==  expected_greeting, \
           f"The returned greeting is: {res_greeting}.\nIt must be: {expected_greeting}."