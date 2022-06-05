# --- Import the required modules / libraries:
from pydantic import BaseModel


# --- Define a schema model for the post using pydantic, which will also do validation:
# --- To be deleted once post and put methods have been migrated to SQLAlchemy driven methods.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Post):
    pass