from fastapi import APIRouter


router = APIRouter(tags = ["Root"])


# --- Create a base route, also called a path operation:
# --- Note app.get = a GET method. "/" is the URL path.
@router.get("/", 
            name = "Root-Level Entry.", 
            summary = "Returns a message indicating that this is not a usable route."
            )

# --- Create a function for the path operation:
# --- Note: async is optional. Only use async if the application (or the function) doesn't need to
# --- communicate with anything else, such as a database. Typically, you would not use this.

async def root():
    return {"greeting": "This is not the endpoint you are looking for!"}