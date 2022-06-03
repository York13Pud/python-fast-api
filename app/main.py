# --- Import the required modules:
from hmac import new
from operator import index
from time import sleep
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine, get_db
import psycopg2

# --- Build the database engine, along with the tables in the models file:
models.Base.metadata.create_all(bind = engine)

# --- Create an instance of FastAPI
app = FastAPI()


# Define a schema model for the post using pydantic, which will also do validation:
class Post(BaseModel):
    # id: int
    title: str
    content: str
    published: bool = True


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
        
        # Attempt to get the records in the database:
        while query_successful is False:
            try:
                cursor.execute("SELECT * FROM posts;")
                print(cursor.fetchone())
                query_successful = True
                
            # Display an error if the query fails:    
            except Exception as error:
                print("error getting data from table")    
                print(error)
                sleep(5)
                
    # Display an error if the connection fails:            
    except Exception as error:
        print("error connecting to DB")
        print(error)
        sleep(5)


# --- Create a base route, also called a path operation:
# Note app.get = a GET method. "/" is the URL path.
# --- Create a function for the path operation:
# Note: async is optional. Only use async if the application (or the function) doesn't need to
# communicate with anything else, such as a database. Typically, you would not use this.
@app.get("/")
async def root():
    return {"greeting": "This is not the endpoint you are looking for!"}


# --- Get all posts:
@app.get("/posts")
def get_all_posts():
    cursor.execute("SELECT * FROM posts ORDER BY id ASC;")
    posts = cursor.fetchall()
    print(posts)
    return {"all_posts": posts}


# --- Get one post record based on its id (path parameter):
@app.get("/posts/{id}")
def get_one_post(id: int):

    try:
        cursor.execute("""SELECT * FROM posts WHERE id = %s""",[id])
        post = cursor.fetchone()
        return {"data": post}
    
    except Exception as error:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")


# --- Create a post:
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def new_post(post: Post):
    
    # Create a new SQL query to write the record:
    cursor.execute("""INSERT INTO posts (title, content, published) 
                      VALUES (%s, %s, %s) 
                      RETURNING *;""",
                      [post.title, post.content, post.published])
    
    # --- Get the details of the new record and assign it to a variable:
    post = cursor.fetchone()
    
    # --- Commit the record to the table. Without this, the record will not be inserted into the table:
    conn.commit()
    
    # --- If the post cannot be created, show an error:
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Post could not be created.")   
    
    # --- Return the value of the post:
    return {"status_code": status.HTTP_201_CREATED,
            "status_detail": "post has been created",
            "data": new_post
            }


# --- Delete a post:
@app.delete("/delete/{id}")
def delete_post(id: int):
    # Create a new SQL query to delete the record:
    cursor.execute("""DELETE FROM posts 
                        WHERE id = %s 
                        RETURNING *;""", [id])
    
    post = cursor.fetchone()
    conn.commit()

    if post == None:
        print("error")
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")
        
    raise HTTPException(status_code = status.HTTP_204_NO_CONTENT)    


# --- Update a post:   
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # Create a new SQL query to write the record:
    cursor.execute("""UPDATE posts 
                      SET title=%s, content=%s, published=%s 
                      WHERE id = %s
                      RETURNING *;""",
                      [post.title, post.content, post.published, id])
    
    # --- Get the details of the new record and assign it to a variable:
    post = cursor.fetchone()
    
    # --- Commit the record to the table. Without this, the record will not be inserted into the table:
    conn.commit()
    
    # --- If the post cannot be created, show an error:
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post {id} not found.")   
    
    # --- Return the value of the post:
    return {"status_code": status.HTTP_200_OK,
            "status_detail": "post has been updated.",
            "data": post
            }


@app.get("/test")
def test(db: Session = Depends(get_db)):
    return {"status": "success"}


