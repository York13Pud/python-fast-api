# --- Import the required modules:
from fastapi.testclient import TestClient
from app.main import app


# --- Create the client to interact with the app:
client = TestClient(app)


# --- Define a function that will test the root url of the app:
def test_root():
    # --- Make a call to the root URL:
    res = client.get("/")
    # --- Print out the contents of the "greeting" key:
    print(res.json().get("greeting"))
    # --- Test to see if the response matches what we expect:
    assert res.json().get("greeting") == "This is not the endpoint you are looking for!"