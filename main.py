# --- Import the required modules:
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

# --- Create an instance of FastAPI
app = FastAPI()

# Define a schema model for the post using pydantic, which will also do validation:
class Post(BaseModel):
    title: str
    content: str
    # published is an optional field as a default is assigned to it.
    published: bool = True
    # This will have a default value of none / null.
    rating: Optional[int] = None

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


# --- Get one post record based on its post_id:
@app.get("/posts/{post_id}")
def get_posts(post_id):
    return {"text_value": post_id}


# --- A post request that uses JSON from the Body of the request
@app.post("/posts")
def get_posts(new_post: Post):
    # --- Show the contents of the new_post pydantic model:
    print(new_post)
    
    # --- Optional: You can convert the pydantic model to a dictionary:
    print(new_post.dict())
    
    return {
                "post_title": new_post.title,
                "post_content": new_post.content,
                "post_published": new_post.published,
                "post_rating": new_post.rating
            }


# --- A simple post request:
@app.post("/test/{text}")
def get_posts(text):
    return {"text_value": text}



