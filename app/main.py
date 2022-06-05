# --- Import the required modules:
from typing import Optional, List
from time import sleep
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine, get_db
from app.schemas import PostCreate, PostResponse
import psycopg2


# --- Build the database engine, along with the tables in the models file:
models.Base.metadata.create_all(bind = engine)


# --- Create an instance of FastAPI
app = FastAPI()


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


# --- Create a base route, also called a path operation:
# --- Note app.get = a GET method. "/" is the URL path.
# --- Create a function for the path operation:
# --- Note: async is optional. Only use async if the application (or the function) doesn't need to
# --- communicate with anything else, such as a database. Typically, you would not use this.
@app.get("/")
async def root():
    return {"greeting": "This is not the endpoint you are looking for!"}


# --- Get all posts:
@app.get("/posts", response_model = List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    # --- Get all the data from the table.
    # --- Note: if you remove .all(), the result will be the actual SQL query that SQLAlchemy translates the ORM request to:
    posts = db.query(models.Post).all()
        
    return posts


# --- Get one post record based on its id (path parameter):
@app.get("/posts/{id}", response_model = PostResponse)
def get_one_post(id: int, db: Session = Depends(get_db)):

    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        return post
    
    except Exception as error:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")


# --- Create a post:
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = PostResponse)
def new_post(post: PostCreate, db: Session = Depends(get_db)):
    
    # --- Method one (more granular): Construct the details for the post request by specific columns:
    # new_post = models.PostCreate( **post.dict() )
                # title = post.title,
                # content = post.content,
                # published = post.published
    # )
    
    # --- Method two (easier for large schema): Construct the details for the post request by taking all the data passed, convert it to a dictionary and
    # --- then strip (**) out the parts that make it a dictionary:
    new_post = models.Post( **post.dict() )
    
    # --- Add the post to the table. You must use commit to write the post tot the table:
    db.add(new_post)
    db.commit()
    
    # --- Use refresh to update new_post with the details of the newly written post:
    db.refresh(new_post)
    
    # --- If the post cannot be created, show an error:
    if not new_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Post could not be created.")   
    
    # --- Return the value of the post:
    return new_post


# --- Delete a post:
@app.delete("/delete/{id}", response_model = PostResponse)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        db.delete(post)
        db.commit()
    
    except Exception as error:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")
            
    raise HTTPException(status_code = status.HTTP_200_OK,
                        detail = f"Post {id} has been deleted.")


# --- Update a post:   
@app.put("/posts/{id}")
def update_post(id: int, post: PostCreate):
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
    return post



