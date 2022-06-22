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

## Documentation

As part of FastAPI, the documentation is auto-generated. You can view the API docs at the below URL's. The difference is one uses SwaggerUI to render and the other uses redoc (respectively) to render the API documentation:

SwaggerUI:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs "http://127.0.0.1:8000/docs")

Redoc:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc "http://127.0.0.1:8000/redoc")

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

## Path Operation Order

Put simply, the order of the paths in you files matters. If you have them set in any old order, you can encounter issues. For example:

* GET HTTP 127.0.0.1/posts
* GET HTTP 127.0.0.1/posts/{post_id}
* GET HTTP 127.0.0.1/posts/all_posts

With the above list of three GET request paths, if you try to call all_posts, it will fail as it actually his /posts/{post_id} as it is above it and the path parameter {post_id} could take the form of all_posts. To remediate this, change the order for the paths in the file so that all_posts is above {post_id}:

* GET HTTP 127.0.0.1/posts
* GET HTTP 127.0.0.1/posts/all_posts
* GET HTTP 127.0.0.1/posts/{post_id}

## Error Codes

### Method One: Hard Code The Error

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

### Method Two: HTTPException

Whilst method one works, there is a cleaner way that uses the HTTPException method to present the HTTP status. Using the example in method one, we can do the same as follows:

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

## Enumerate Function

Enumerate reads the list and produces a sequence number for each dictionary / entry in the list with the first number starting at 0.

For example, the below will take a list called my_posts, along with an id parameter / argument, enumerate it and if the id matches one of the dictionary id's, it will return the index number.

``` python
def find_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
```

## Python Packaging

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

## Databases

By default, once PostgreSQL is installed, it creates a default database called 'postgres'.

Examples of datatypes for PostgreSQL:

Numeric: integer, decimal and precision.
Text: varchar and text.
Bool: boolean.
Sequence: array.

Use unique constraints to enforce a column has a unique value.

NULL constraints allow you to require a field to have a value and cannot be blank.

### Sample SQL Queries

#### SELECT and WHERE

Get products named Pencil or Remote:

``` sql
SELECT name, price, stock_level
FROM products 
WHERE name='Pencil' OR name='Remote';
```

Get products that have no stock:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level=0;
```

Get products that have stock higher than 0:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0;
```

#### ORDER BY and ASC and DESC

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

Get products that have stock higher than 0 and sort by stock level descending and price ascending if there is a conflict with two records having the same stock level:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0 
ORDER BY stock_level DESC, price ASC;
```

#### AND & OR

Get products that have stock higher than 0, with a price higher than 10 and sort by stock level descending:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0 AND price >= 10
ORDER BY stock_level DESC;
```

Get products that have stock higher than 100, or has a name of Pencil and sort by stock level descending:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 100 OR name = 'Pencil'
ORDER BY stock_level DESC;
```

#### IN Operator

The IN operator allows you to pass an array of values to query rather than typing out a lot of OR statements. For example:

Get products that have an id of 1, 2 or 3:

Method one, multiple OR operations:

``` sql
SELECT id, name, price, stock_level 
FROM products 
WHERE id = 1 OR id = 2 OR id = 3
ORDER BY stock_level DESC;
```

Method two, using the IN operator:

``` sql
SELECT id, name, price, stock_level 
FROM products 
WHERE id IN (1,2,3)
ORDER BY stock_level DESC;
```

#### LIKE Operator

The LIKE operator allows you to perform queries that search for a value based on partial information. For example:

Find all records that contain the word TV in the name column:

``` sql
SELECT id, name, price, stock_level 
FROM products 
WHERE name LIKE '%TV%'
ORDER BY stock_level DESC;
```

Find all records that end with the word TV in the name column:

``` sql
SELECT id, name, price, stock_level 
FROM products 
WHERE name LIKE '%TV'
ORDER BY stock_level DESC;
```

Find all records that start with the word TV in the name column:

``` sql
SELECT id, name, price, stock_level 
FROM products 
WHERE name LIKE 'TV%'
ORDER BY stock_level DESC;
```

You can combine LIKE with the NOT operator to return a reverse of what was searched for. For example:

Find all records that don't contain the word TV in the name column:

``` sql
SELECT id, name, price, stock_level 
FROM products 
WHERE name NOT LIKE '%TV%'
ORDER BY stock_level DESC;
```

#### LIMIT Operator

You can limit the number of records returned by using the LIMIT operator. For example:

Show only the first 5 items that are found from this query:

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0
ORDER BY stock_level DESC
LIMIT 5;
```

#### OFFSET Operator

OFFSET can be used to ignore the first x number of results that have been found and show x results from what you offset by. For example:

Show only 5 items that are found from this query with the first two being skipped (5 results will show bu they will be 3 to 7 as 1 and 2 are skipped (offset)):

``` sql
SELECT name, price, stock_level 
FROM products 
WHERE stock_level > 0
ORDER BY stock_level DESC
LIMIT 5
OFFSET 2;
```

### Sample SQL Data Insertions

To add data to a table, you use the INSERT operator. For example:

Add a record to the table named products:

``` sql
INSERT INTO products 
    (name, price, on_sale, stock_level)
VALUES 
    ('Webcam', 100, false, 2348);
```

Note: The order in the VALUES array must match the order in the INSERT (first) array. Also, make sure that the datatypes are correct for each column / value.

If the insertion is successful, will get a message similar to the following:

``` console
INSERT 0 1

Query returned successfully in 25 msec.
```

If it wasn't successful, you will get an error indicating where the issue is in the query.

If you would like to see the inserted data after it has been added, you can use the RETURNING operator to do this. For example:

Create a new record in the products table and return a few of the columns instead of a success message:

``` sql
INSERT INTO products 
    (name, price, on_sale, stock_level)
VALUES 
    ('Webcam', 100, false, 2348)
RETURNING id, name, price, stock_level;
```

To insert multiple records, you can pass multiple array in the values section:

``` sql
INSERT INTO products 
    (name, price, on_sale, stock_level)
VALUES 
    ('Webcam',100,false,2348),
    ('Tractor',1000000,false,0),
    ('PS5',450,false,1)
RETURNING id, name, price, stock_level;
```

### Delete Records

To delete a record from the products table:

``` sql
DELETE FROM products WHERE id = 12;
```

To delete a record from the products table and see what it was before it was deleted, you can use the returning operator:

``` sql
DELETE FROM products WHERE id = 12 RETURNING id, name;
```

To delete multiple records from the products table using the id column:

``` sql
DELETE FROM products WHERE id IN (1,2);
```

To delete multiple records based on a criteria rather than a fixed record, you can do the following (delete all products with price > 100):

``` sql
DELETE FROM products WHERE price > 100 RETURNING id, name;
```

### Updating Records

To update a record, you can do this using the UPDATE operator and SET operator. For example:

``` sql
UPDATE products SET name='USB Microphone', price=123 WHERE id = 5 RETURNING id, name, price;
```

To update multiple records by a criteria, it's simple to do. For example:

``` sql
UPDATE products SET on_sale=true WHERE id > 6  RETURNING id, name, price, on_sale;
```

### Composite Keys

This is a primary key that spans multiple columns. For example, post_id and user_id can compose a composite key for a likes table to stop a user from liking a post more than once.

### Psycopg2

Psycopg2 (or Psycopg3) is a driver to allow Python to interact with a PostgreSQL database by using standard SQL commands, just like you normally would with say pgAdmin or the pgsql CLI.

To use it, you need to install it via pip, import the module and then create a connection to the database server.

``` python
# --- Import the required modules:
# --- RealDictCursor will show the column names for each column in a table as part of the response and format it as JSON.
import psycopg2
from psycopg2.extras import RealDictCursor

# --- Setup the connection:
conn = psycopg2.connect(host="hostname or ip_address", 
                        dbname="database_name", 
                        user="usernames", 
                        password="password",
                        cursor_factory=RealDictCursor
                        )
# --- Create a cursor to allow execution of commands:
cursor = conn.cursor()
print("Connected to DB")
```

Once the connection is made, you can start to pass queries to it. For example, get all the records in a table:

``` python
# --- Get all posts:
@app.get("/posts")
def get_all_posts():
    # --- Query the table to return all of the records stored in it:
    cursor.execute("SELECT * FROM posts;")

    # --- Define a variable that will grab all of the records that are returned from the last cursor.execute command:
    posts = cursor.fetchall()
    
    # --- Return all of the records as JSON:
    return {"all_posts": posts}
```

Another example would be to delete a record. The below example covers that but you can change out the SQL query for other actions, such as updating a record:

``` python
@app.delete("/delete/{id}")
def delete_post(id: int):
    # Create a new SQL query to delete the record:
    cursor.execute("""DELETE FROM posts 
                        WHERE id = %s 
                        RETURNING *;""", [id])
    # --- Define a variable that will grab the record from the last cursor.execute command. We use fetchone instead of fetchall as we should only ever get one back:
    post = cursor.fetchone()
    
    # --- Commit the query to the table. If you don't do this the record will not be deleted from the table.
    conn.commit()

    if post == None:
        print("error")
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")

    # --- Set the HTTP return code to 204 to indicate to the API requester that the record has been deleted:
    raise HTTPException(status_code = status.HTTP_204_NO_CONTENT)  
```

Note: HTTP 204 will return no data back to the API requester. It will only return back a 204.

### Object Relational Mapper (ORM)

An ORM is a layer of abstraction that sits between Python and the database. In effect, it will take code that is Python-based, convert it into SQL and then run those queries against the database and return whatever is needed in a Python friendly (dictionaries / lists) format. As a result, you no longer need to write out any SQL queries!

For Python, we would typically use SQLAlchemy as our ORM.

#### Install SQLAlchemy

``` console
pip install sqlalchemy
```

You will also need a driver for Python to connect to PostgreSQL. We will use psycopg2 again for this.

``` console
pip install psycopg2-binary
```

#### Setup Database Connection and Tables

Once installed, you would typically create two files:

* database.py - This file contains the code that is used to connect to the database server and the required database(s).
* models.py - This file contains all of the table schemas for the database you are using.

These files will then be imported into the main.py file, along with the following code to allow you to use the database. Place it above the line where you create the app:

``` python
# --- Build the database engine, along with the tables in the models file:
models.Base.metadata.create_all(bind = engine)
```

Note: SQLAlchemy will not update tables in the models if the table already exists. If schema changes need to be made, this is called a migration and is handled by another library called Alembic.

### Route File Separation and Path Prefix

You can separate the routes / path operation up into different files by placing them in a routes folder in you apps directory.

You can also use a path prefix with the file so that you don't have to type out a path each time. You also don't call a variable / constant for the path as it is done when you call the APIRouter.

From there, you will need to make some changes to each of the routes and import the APIRouter class from FastAPI. An example route file (post.py) is shown below:

``` python
from app import models
from app.database import get_db
from app.schemas import PostCreate, PostResponse

from fastapi import status, HTTPException, Depends, APIRouter

from typing import List

from sqlalchemy.orm import Session

# --- Create a router variable that uses the APIRouter class:
router = APIRouter(
    # --- prefix will prefix /user to every route in this file. That way you don't
    # --- need to use /user on every rout / path operation:
    prefix="/post"
    )

# --- Get all posts:
@router.get("/", response_model = List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    # --- Get all the data from the table.
    # --- Note: if you remove .all(), the result will be the actual SQL query that SQLAlchemy translates the ORM request to:
    posts = db.query(models.Post).all()
        
    return posts
```

You then need to make a few changes to the main.py file:

``` python
# --- import the route files from the routers folder in the app package (folder):
from app.routers import post, user

# --- Reference the files that contain the routes / path operations for the application:
app.include_router(post.router)
app.include_router(user.router)
```

### API Documentation Grouping

As part of using route files, you can also group you API's up so that the documentation produced by SwaggerUI will group up the API actions by tag names. For example, all of the routes / path operations in the file called post.py should be grouped up using the name Posts:

``` python
# --- Create a router variable that uses the APIRouter class:
router = APIRouter(
    # --- prefix will prefix /user to every route in this file. That way you don't
    # --- need to use /user on every rout / path operation:
    prefix = "/post",
    tags = ["Posts"]
    )
```

You can use multiple tags if you wish as it is a list that is passed.

### JWT: JSON Web Token Authentication

JSON Web Tokens (JWT) are an open, industry standard (RFC 7519) method for representing claims securely between two parties.

00-jwt-token-auth-flow

01-jwt-token-structure:

* The payload part of the token can be read by other actors. Don't include any confidential info in there.
* The token is not encrypted.

### Environment Variables

Use these instead of hard coding things like passwords into the code.

``` console
export MY_ENV_VAR="hello"
echo $MY_ENV_VAR
```

To access these in Python, you need to use the os module:

``` python
import os

print(os.getenv("MY_ENV_VAR"))
```

You can use pydantic and a class to construct an object with all of the environment variables in so that you can access them but also have pydantic verify they exist. If they don't, it will error.

Pydantic BaseSettings is used to read environment variables. The name of the environment variable be be in uppercase or lowercase. Pydantic will convert it to uppercase to match that of the environment variable as they are in uppercase at the O/S level.

For example:

``` python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # --- Read the value of MY_ENV_VAR. If it is not found, default to localhost
    MY_ENV_VAR: str = "localhost"
    
settings = Settings()

print(settings.MY_ENV_VAR) 
# --- prints hello or (if my_env_var is not defined) localhost.
```

Rather than setting the environment variables (for dev at least, don't do this for prod), you can use and environments variable file. This file is a simple one that contains the name and value of each environment variable.

The file name is typically .env. For example:

``` python
# --- .env file.
MY_ENV_VAR=hello
```

You then just need to add a Config class to the Settings class that will then fill the matching variable(s) in the .env file:

``` python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # --- Read the value of MY_ENV_VAR. If it is not found, default to localhost
    MY_ENV_VAR: str = "localhost"
    
    class Config:
        """This class will import all of the environment variables that you have set"""
        env_file = ".env"

settings = Settings()

print(settings.MY_ENV_VAR)
```

### Alembic

Alembic is a database migration tool. Database migrations allow for the tracking of incremental changes to the schema / models in a given database.

Alembic can tie in with SQLAlchemy to pull the models into it and generate / update the tables in that database.

To use alembic, you first need to install it:

``` console
pip install alembic
```

Once it is installed, it will allow you to run the alembic command. You can see what arguments you can pass into the command by looking at the help:

``` console
alembic --help
```

The first step to using alembic for database migration tracking is to initialise it. Think of it like initialising a local git repository. In the below example, change ```name-of-folder``` to whatever you want:

``` console
alembic init <name-of-folder>
```

Make notes for file changes to make to env.py and config.ini

Once the env.py and config.ini files have been setup, you can start to use alembic to track your database. To begin, a revision will need to be created:

``` console
alembic revision --message "create posts table"
```

A new folder in the alembic folder will be created called versions. In that folder will be a file that looks similar to this:

``` console
785b3ca90a20_create_posts_table.py
```

Open the file it creates. In the file there will be two functions, one called upgrade and another called downgrade. Each of these sections are used to perform an action against the database. If you are adding to the database, use the upgrade function. To remove an existing entity in the database, use the downgrade function.

To create a new table that is tracked, in the upgrade section of the file, add the code to create the table. The following example will create a new table called posts with two columns. It also has a downgrade block in there that will drop the table:

``` python
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '785b3ca90a20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", 
                    sa.Column("id", 
                              sa.Integer, 
                              nullable = False, 
                              primary_key = True)), \
                    sa.Column("title", 
                              sa.String, 
                              nullable = False)

def downgrade() -> None:
    op.drop_table("posts")
```

Once the code has been entered as required for the database, you can then run the upgrade or downgrade. Before that, make a note of the text in the revision variable as you will need it.

To run an upgrade, run the following command:

``` console
alembic upgrade 785b3ca90a20
```

This will execute the upgrade function in the revision file. The downgrade function will not be run. If you did want to run the downgrade function, the command for that is:

``` console
alembic downgrade 785b3ca90a20
```

When you run the upgrade command, a new table called alembic will appear in the database (if it doesn't already exist). This will have a single table that tracks what revision was last run successfully.

To view what the most recent revision file is, you can run:

``` console
alembic head
```

### CORS

CORS, or Cross Origin Resource Sharing allows you to make requests from a web browser on one domain to a server on a different domain.

By default, the FastAPI dev server will only permit access to requests sent from the local system.

To enable FastAPI to use CORS, you need to perform the following:

``` python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
```

To test CORS, open up a browser and go to one of the domains in the allowed list. From there, go to the developer tools (F12 for most), click console and enter:

``` javascript
fetch('http://localhost:8000/').then(res=>res.json()).then(console.log)
```

If CORS is setup correctly, the response will be whatever was set at the root level route that was set. If not, you will likely get a message indicating a CORS policy has blocked the request. An example is shown below:

``` console
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at https://play.google.com/log?format=json&hasfast=true&authuser=0. (Reason: CORS request did not succeed). Status code: (null).
```

The likely hood is that the domain you are connecting from is setup incorrectly in the allowed list or the request was made from the wrong domain. Check the URL that is showing as it might have been redirected.

### Gunicorn

It is a process manager that will be used to run the FastAPI app.

Install the package with pip, along with some dependencies:

``` console
pip install uvloop uvtools httptools gunicorn
```

Once installed, you can run the app:

``` console
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind <ip-address:port>
```

The issue with the above is that it is a runtime command, meaning it will be active whilst you are logged in and running it. Instead, you can create a systemd service to start the process at system startup and manage it via systemd.

An example systemd service is shown below. The filename will be fastapi.service:

``` bash
[Unit]
Description=demo fastapi application
After=network.target

[Service]
User=neil
Group=neil
WorkingDirectory=/home/neil/app/source/
Environment="PATH=/home/neil/app/venv/bin"
EnvironmentFile=/home/neil/.env
ExecStart=/home/neil/app/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Once the file is created, the service can be started:

``` console
sudo systemctl start fastapi.service
```

The service will then start. To have the service start at whenever the system is restarted, run the following command:

``` console
sudo systemctl enable fastapi.service
```

### NGINX

Once Gunicorn is configured, the next step is to setup NGINX to act as a proxy server that will perform SSL termination as well.

First, install it on Ubuntu and then enable it to startup when the system is rebooted:

``` console
sudo apt install nginx && sudo systemctl enable nginx
```

Next, edit the /etc/nginx//sites-available/defaul file and replace the location section with the below:

``` console
location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_redirect off;
}
```

Restart NGINX:

``` console
sudo systemctl restart nginx
```

Open a browser and it should show the default route from the FastAPI application.

### Testing

Testing will be done with pytest. First, install it:

``` console
pip install pytest
```

Place all of the tests in a folder named tests (at the root) and name the files either test_*.py or *_test.py with * being whatever you want to call it. PyTest will look for files with these name formats in the tests folder by default. You can pass the filename to pytest manually if you don't want to follow that naming convention.

Also, with auto-test discovery, the name of the functions in the test files nee to start with test_.

An example of a simple test is shown below. The test will perform a basic add operation:

``` python
from app.calculations import add_test

def test_add():
    print("Testing add function")
    total_sum = add_test(5, 3)
    # True is ok, False will error
    assert total_sum == 8
    
test_add()
```

The assert method will perform a true / false check for a desired outcome. In the above example, the expected result of 5+3 is 8, which will result in True. This will result in the test passing.

PyTest is a command line tool. You use it by running ```pytest``` at the command line. The result of this should be true and look like the following output:

``` console
============================== test session starts ==============================

platform darwin -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/neil/Documents/training/programming/python/python-fast-api
plugins: anyio-3.6.1
collected 1 item

tests/test_basic.py .                                                      [100%]

==============================  1 passed in 0.02s  ==============================
```

To explain a little about the above:

* Collected 1 item indicates the number of tests found.
* The . after tests/test_basic.py indicates the number of tests run in that file. If there were two tests, it would show .. instead. Green is ok and red is a failed test.

It is recommended to use ```pytest -v``` instead as the verbose detail is more useful. A sample output is shown below:

``` console
============================== test session starts ==============================

platform darwin -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0 -- /Users/neil
/Documents/training/programming/python/python-fast-api/venv/bin/python3

cachedir: .pytest_cache
rootdir: /Users/neil/Documents/training/programming/python/python-fast-api
plugins: anyio-3.6.1

collected 2 items         

tests/test_basic.py::test_add PASSED                                     [ 50%]
tests/test_basic.py::test_sub PASSED                                     [100%]

============================== 2 passed in 0.03s ==============================
```

The main difference is that rather than showing a . for each test, it will show a list of each test that was run. This is much more useful.

A point of note; print statements, by default are not shown on the test output. To allow this, add the -s switch to the pytest command when you run it.

The examples shown so far have been basic and limited to only one test. But what do we do if we need to run multiple tests using the same function?

What can be done is to use a wrapper function called pytest.mark.parametrize to pass a list of tuples, with each tuple having the test values to use in, including any expected results. For example, the below will perform three additions using a function:

``` python
import pytest

@pytest.mark.parametrize("num_1, num_2, result", [(3,2,5),
                                                  (5,2,7),
                                                  (8,7,15)
                                                 ])
def test_add(num_1, num_2, result):
    total_sum = num_1 + num_2
    # True is ok (green), False will error (red)
    assert total_sum == result
```

When you run it with ```pytest -v```, the below is the expected output:

``` console
============================== test session starts ==============================
platform darwin -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0 -- /Users/neil/
Documents/training/programming/python/python-fast-api/venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/neil/Documents/training/programming/python/python-fast-api
plugins: anyio-3.6.1
collected 3 items

tests/test_basic.py::test_add[3-2-5] PASSED                                [ 33%]
tests/test_basic.py::test_add[5-2-7] PASSED                                [ 66%]
tests/test_basic.py::test_add[8-7-15] PASSED                               [100%]

==============================  3 passed in 0.03s  ==============================
```

When you work with tests that make use of a class, rather than initialising it each time in a function, you can use a fixture initialise it and then pass that to the functions. This will save time writing out the code multiple time and you may need to initialise a number of things prior.

For example, a class (not shown) named BankAccount is used by multiple functions:

``` python
import pytest

from bankaccount import BankAccount

@pytest.fixture
def zero_bank_balance():
    # --- The default value for balance is 0 so no need to pass it:
    return BankAccount()


@pytest.fixture
def bank_balance():
    return BankAccount(blance=50)


def test_bank_default_balance(zero_bank_balance):
    assert zero_bank_balance.balance == 0


def test_bank_set_initial_balance(bank_balance):
    assert bank_balance.balance == 50


def test_bank_withdraw(bank_balance):
    bank_balance.withdraw(30)
    assert bank_balance.balance == 20
```

You can also use parameterisation along with fixtures. For example:

``` python

@pytest.mark.parametrize("deposit, withdraw, result", [(200,100,100),
                                                       (300,150,150)
                                                      ])
def test_bank_transactions(zero_bank_balance, deposit, withdraw, result):
    bank_balance.deposit(deposit)
    bank_balance.withdraw(withdraw)
    assert zero_bank_balance.deposit == result
```

In the event that you need to perform a test that will fail and raise an error, which is the expected outcome, you can use pytest.raises. For example:

``` python
def test_insufficient_funds(bank_balance):
    with pytest.raises(Exception):
        bank_account.withdraw(200)
```