# --- Import the required modules:
from email.policy import HTTP
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

# --- Create an instance of FastAPI
app = FastAPI()

# Define a schema model for the post using pydantic, which will also do validation:
class Post(BaseModel):
    id: int
    title: str
    content: str
    # published is an optional field as a default is assigned to it.
    published: bool = True
    # This will have a default value of none / null.
    rating: Optional[int] = None


# --- Create a variable with an empty list to store the posts (temp solution until DB ready.)
my_posts = [{"id": 1, "title": "blog post 1", "content": "content of blog post 1"},
            {"id": 2, "title": "blog post 2", "content": "content of blog post 2"}]

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
def get_all_posts():
    return {"all_posts": my_posts}


# --- Get one post record based on its post_id (path parameter):
@app.get("/posts/{post_id}")
def get_one_post(post_id: int):
    print(type(post_id))
    for post in my_posts:
        if post["id"] == post_id:
            return {"post_data": post}
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"Post ID {post_id} not found")


# --- A post request that uses JSON from the Body of the request:
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def new_post(new_post: Post):
    
    # --- Add the post to the my_posts list:
    my_posts.append(new_post.dict())

    # --- Return the value of the post:
    return {"status_code": status.HTTP_201_CREATED,
            "status_detail": "post has been created",
            "data": new_post.dict()}


@app.delete("/delete/{post_id}")
def delete_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            # --- Delete the post from the list:
            my_posts.remove(post)
            raise HTTPException(status_code = status.HTTP_202_ACCEPTED,
                                detail = f'Post {post["id"]} has been deleted')
    
    # --- If record can't be found, raise a 404    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"Post ID {post_id} not found")


# --- A simple post request:
@app.post("/test/{text}")
def get_posts(text):
    return {"text_value": text}





