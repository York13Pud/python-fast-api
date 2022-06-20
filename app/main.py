# --- Import the required modules:
from app.cors.allow import allowed_origins
from app.database import engine
from app.models import models
from app.routers import auth, post, root, user, vote

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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


# --- Setup FastAPI to use CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Reference the files that contain the routes / path operations for the application:
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(root.router)
app.include_router(user.router)
app.include_router(vote.router)
