# FastAPI Notes

## Basics.

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

## Documentation.

As part of FastAPI, the documentation is auto-generated. You can view the API docs at the below URL's. The difference is one uses SwaggerUI to render and the other uses redoc (respectively) to render the API documentation:

SwaggerUI:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs "http://127.0.0.1:8000/docs")

Redoc:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc "http://127.0.0.1:8000/redoc")


## Post Request / Path Operation Example.

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

## Post Request Data Validation.

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

## CRUD Operations.

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

## Path Operation Order.

Put simply, the order of the paths in you files matters. If you have them set in any old order, you can encounter issues. For example:

* GET HTTP 127.0.0.1/posts
* GET HTTP 127.0.0.1/posts/{post_id}
* GET HTTP 127.0.0.1/posts/all_posts

With the above list of three GET request paths, if you try to call all_posts, it will fail as it actually his /posts/{post_id} as it is above it and the path parameter {post_id} could take the form of all_posts. To remediate this, change the order for the paths in the file so that all_posts is above {post_id}:

* GET HTTP 127.0.0.1/posts
* GET HTTP 127.0.0.1/posts/all_posts
* GET HTTP 127.0.0.1/posts/{post_id}

## Error Codes.

### Method One: Hard Code The Error.

You can specify an HTTP error code for when something occurs. In the below example, we will return a 404 (not found) if the post_id is not matched:

``` python
# --- Get one post record based on its post_id (path parameter):
@app.get("/posts/{post_id}")
def get_one_post(post_id: int, response: Response):
    print(type(post_id))
    for post in my_posts:
        if post["id"] == post_id:
            return {"post_data": post}
    
    error = response.status_code = status.HTTP_404_NOT_FOUND       
    return { "error": f"Post ID {post_id} not found" }
```
response: Response tracks the status code and we can set this to any valid HTTP code.

NOTE: The above requires Response and status to be imported from the fastapi module.

In the event that the post_id is not found, the error returned will look like the below:

``` json
{
    "error": "Post 3 not found",
    "status": 404
}
```

In addition, the software that you are using will show 404 as the HTTP status.

### Method Two: HTTPException.

Whilst method one works, there is a cleaner way that uses the HTTPException method to present the HTTP staus. Using the example in method one, we can do the same as follows:

``` python
# --- Get one post record based on its post_id (path parameter):
@app.get("/posts/{post_id}")
def get_one_post(post_id: int):
    print(type(post_id))
    for post in my_posts:
        if post["id"] == post_id:
            return {"post_data": post}
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"Post ID {post_id} not found")
```

In the event that the post_id is not found, the error returned will look like the below:

``` json
{
    "detail": "Post ID 3 not found"
}
```

## Enumerate Function.

Enumerate reads the list and produces a sequence number for each dictionary / entry in the list with the first number starting at 0. 

For example, the below will take a list called my_posts, along with an id parameter / argument, enumerate it and if the id matches one of the dictionary id's, it will return the index number.

``` python
def find_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
```

## Python Packaging.

As part of Python, you can create packages that contain code to use in you API. A common practice is to use a folder to put the code in and also add a file called \_\_init\_\_.py. FastAPI / Python will then treat this folder as a package. An example would be to create a folder called app and then put some, or all of your code in there, along with an \_\_init\_\_.py file (which can be left empty if needed):

``` structured-text
my_application
|
|___ README.md
|___ .gitignore
|___ requirements.txt
|
|___venv
|   |___ venv files
|
|___app
|   |___ __init__.py
|   |___ main.py
|   |___ other-required-files
|
-

```
One additional thing you will need to do is to change the uvicorn path for the start file, if you moved it. For example, if we moved main.py into the app folder, we would start it by replacing main:app with app.main:app:

``` console
uvicorn app.main:app --reload
```

## Databases.

By default, once PostgreSQL is installed, it creates a default database called 'postgres'.

Examples of datatypes for PostgreSQL:

Numeric: integer, decimal and precision.
Text: varchat and text.
Bool: boolean.
Sequence: array.

Use unique constraints to enforce a column has a unique value.

NULL constraints allow you to require a field to have a value and cannot be blank.

### Sample SQL Queries.

#### SELECT and WHERE.
Get products named Pencil or Remote:

``` sql
SELECT name, price, stock_level FROM products WHERE name='Pencil' OR name='Remote';
```

Get products that have no stock:

``` sql
SELECT name, price, stock_level FROM products WHERE stock_level=0;
```

Get products that have stock higher than 0:

``` sql
SELECT name, price, stock_level FROM products WHERE stock_level > 0;
```

#### ORDER BY and ASC and DESC.


Get products that have stock higher than 0 and sort by stock level ascending:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0 
ORDER BY stock_level ASC;
```

Get products that have stock higher than 0 and sort by stock level descending:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0 
ORDER BY stock_level DESC;
```

#### AND & OR

Get products that have stock higher than 0, with a price higher than 10 and sort by stock level descending:

``` pgsql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0 AND price >= 10
ORDER BY stock_level DESC;
```