# --- Import the required modules / libraries:
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


######## --- Requests --- ########

# --- Define a schema model for the post using pydantic, which will also do validation:
# --- To be deleted once post and put methods have been migrated to SQLAlchemy driven methods.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(Post):
    pass


class User(BaseModel):
    email: EmailStr
    password: str
    
    
class UserCreate(User):
    pass


class UserLogin(User):
    pass
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    

class Voting(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)









######## --- Responses --- ########

# --- Create a class that will be used by the create_post function to return a response that has been validated
# --- and type checked before returning it to the user. Notice that there are only two fields. That is because
# --- PostResponse is extending from Post, which means that in addition to what is in the Post class, PostResponse
# --- will be adding id and created_at to the response, totalling five fields:
class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # --- This class will allow the pydantic library to return back a dictionary format:
    class Config:
        orm_mode = True


class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserCreateResponse
    # --- This class will allow the pydantic library to return back a dictionary format:
    class Config:
        orm_mode = True

class AllPostResponse(Post):
    id: int
    owner_id: int
    created_at: datetime
    # --- This class will allow the pydantic library to return back a dictionary format:
    class Config:
        orm_mode = True
        
class AllPostsResponseVotes(BaseModel):
    Post: PostResponse
    votes: int
    # --- This class will allow the pydantic library to return back a dictionary format:
    class Config:
        orm_mode = True    
        
class UserDetailsResponse(UserCreateResponse):
    pass