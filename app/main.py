# --- Import the required modules:
from app.models import models
from app.database import engine
from app.routers import auth, post, root, user

from fastapi import FastAPI


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


# --- Reference the files that contain the routes / path operations for the application:
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(root.router)
app.include_router(user.router)


# --- Create a base route, also called a path operation:
# --- Note app.get = a GET method. "/" is the URL path.
# @app.get("/")

# --- Create a function for the path operation:
# --- Note: async is optional. Only use async if the application (or the function) doesn't need to
# --- communicate with anything else, such as a database. Typically, you would not use this.

# async def root():
#     return {"greeting": "This is not the endpoint you are looking for!"}






