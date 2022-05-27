# FastAPI Notes

## Basics

A simple app example with a single get path operation:

``` python
# --- Import the required modules:
from fastapi import FastAPI

# --- Create an instance of FastAPI
app = FastAPI()

# --- Create a base route, also called a path operation:
# --- Note app.get = a GET method. "/" is the URL path.
@app.get("/")

# --- Create a function for the path operation:
# --- Note: async is optional. Only use async if the application (or the function) doesn't need to
# --- communicate with anything else, such as a database. Typically, you would not use this.
async def root():
    return {"greeting": "Hello World!"}
```
NOTE: Use plural, not singular versions for the path name. For example, use /users rather than /user.

FastAPI uses uvicorn to run the application as a web server. To run the app, run the below in the terminal:

``` console
uvicorn main:app --reload
```

* uvicorn: The command for the server to run the app.
* main: The name of the file that has the start code for the application.
* app: The name you gave to the application that creates a FastAPI instance.
* --reload: This is optional. It will check for file saves and reload the server when it detects any.

Once the server is running, it will tell you what the URL it is running on and the TCP port. This is typically:

[http://127.0.0.1:8000](http://127.0.0.1:8000 "http://127.0.0.1:8000")

In addition, you can view the API docs at the below URL (it uses SwaggerUI to render):

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs "http://127.0.0.1:8000/docs")

## Post Request / Path Operation Example

``` python
# --- A simple post request:
@app.post("/test/{text}")
def get_posts(text):
    return {"text_value": text}
```

The post request will have a requirement to pass some text as the {text} parameter and the above will return it as a JSON response.

A more practical example:

``` python
@app.post("/createpost")
def get_posts(payload: dict = Body(...)):
    return {
                "post_title": payload["title"],
                "post_heading": payload["heading"]
            }
```
A post request that uses JSON from the Body of the request to be set as a dictionary and then returned back with different key names.

## Post Request Data Validation

Use the pydantc module to allow you to create a schema using a class. When called, it will also do data validation. For example:

``` python
from pydantic import BaseModel

# --- Define a schema model for the post using pydantic, which will also do validation:
class Post(BaseModel):
    title: str
    content: str
    # --- published is an optional field as a default is assigned to it.
    published: bool = True
    # --- This will have a default value of none / null.
    rating: Optional[int] = None

# --- A post request that uses JSON from the Body of the request
@app.post("/createpost")
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
```

## CRUD Operations

Create = Post

``` python
@app.post("/posts")
```

Read = Get

``` python
@app.post("/posts")
# OR (specify a specific post_id)
@app.post("/posts/{post_id}")
```

Update = Put (update entire record) / Patch (update part of a record)

``` python
@app.put("/posts/{post_id}")
```

Delete = Well, erm, delete a record!! :-)

``` python
@app.delete("/posts/{post_id}")
```

