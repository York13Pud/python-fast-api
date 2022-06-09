# --- Import the required modules:
from app import models
from app.database import engine
from app.routers import auth, post, user

from fastapi import FastAPI

from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor


# --- Build the database engine, along with the tables in the models file:
models.Base.metadata.create_all(bind = engine)


# --- Create an instance of FastAPI
app = FastAPI(
    # --- These details will be shown on the API documentation:
    title = "Blog Post API Reference",
    description ="This API is used for interacting with a database containing blog posts and more.",
    version = "1.0.1",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        }
        ]
)


# --- Setup the connection to the database:
connection_successful = False
query_successful = False


# --- Attempt to connect to the database:
while connection_successful is False:
    try:
        # --- Setup the connection:
        conn = psycopg2.connect(host="localhost", 
                                dbname="fastapi", 
                                user="postgres", 
                                password="",
                                cursor_factory=RealDictCursor
                                )
        
        # --- Create a cursor to allow execution of commands:
        cursor = conn.cursor()
        print("Connected to DB")
        
        # --- Set connection_successful to True to stop the loop:
        connection_successful = True
        
        # --- Attempt to get the records in the database:
        while query_successful is False:
            try:
                cursor.execute("SELECT * FROM posts;")
                print(cursor.fetchone())
                query_successful = True
                
            # --- Display an error if the query fails:    
            except Exception as error:
                print("error getting data from table")    
                print(error)
                sleep(5)
                
    # --- Display an error if the connection fails:            
    except Exception as error:
        print("error connecting to DB")
        print(error)
        sleep(5)


# --- Reference the files that contain the routes / path operations for the application:
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# --- Create a base route, also called a path operation:
# --- Note app.get = a GET method. "/" is the URL path.
@app.get("/")

# --- Create a function for the path operation:
# --- Note: async is optional. Only use async if the application (or the function) doesn't need to
# --- communicate with anything else, such as a database. Typically, you would not use this.

async def root():
    return {"greeting": "This is not the endpoint you are looking for!"}






