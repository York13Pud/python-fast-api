# --- Import the required modules:
from fastapi import FastAPI

# --- Create an instance of FastAPI
app = FastAPI()

# --- Create a base route, also called a path operation:
# Note app.get = a GET request.
@app.get("/")
# --- Create a function for the path operation:
# Note: async is optional. Only use async if the application (or the function) doesn't need to
# communicate with anything else, such as a database. Typically, you would not use this.
async def root():
    return {"greeting": "Hello World!"}

# 40:45