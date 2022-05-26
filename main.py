# --- Import the required modules:
from fastapi import FastAPI
from fastapi.params import Body
# --- Create an instance of FastAPI
app = FastAPI()

# --- Create a base route, also called a path operation:
# Note app.get = a GET method. "/" is the URL path.
@app.get("/")

# --- Create a function for the path operation:
# Note: async is optional. Only use async if the application (or the function) doesn't need to
# communicate with anything else, such as a database. Typically, you would not use this.
async def root():
    return {"greeting": "Hello World!"}


# --- Get all posts:
@app.get("/posts")
def get_posts():
    return {"data": "payload"}

# --- A simple post request:
@app.post("/test/{text}")
def get_posts(text):
    return {"text_value": text}


# --- A post request that uses JSON from the Body of the request
# --- to be set as a dictionary and then returned back with different key names.
@app.post("/createpost")
def get_posts(payload: dict = Body(...)):
    return {
                "post_title": payload["title"],
                "post_heading": payload["heading"]
            }