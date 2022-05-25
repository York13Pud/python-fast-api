# --- Import the required modules:
from fastapi import FastAPI

# --- Create an instance of FastAPI
app = FastAPI()

# --- Create a base route, also called a path operation:
# Note app.get = a GET request.
@app.get("/")
async def root():
    return {"message": "Hello World!"}