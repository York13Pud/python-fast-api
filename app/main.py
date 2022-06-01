# --- Import the required modules:
from hmac import new
from operator import index
from time import sleep
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

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



# --- Create a variable with an empty list to store the posts (temp solution until DB ready.)
my_posts = [{"id": 1, "title": "blog post 1", "content": "content of blog post 1"},
            {"id": 2, "title": "blog post 2", "content": "content of blog post 2"}]


# --- Find the index of the post in the list.
def find_index(id):
    # --- Enumerate reads the list and produces a sequence number for each dictionary in the list
    # --- starting at 0.
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


# --- Create a base route, also called a path operation:
# Note app.get = a GET method. "/" is the URL path.
@app.get("/")

# --- Create a function for the path operation:
# Note: async is optional. Only use async if the application (or the function) doesn't need to
# communicate with anything else, such as a database. Typically, you would not use this.
async def root():
    return {"greeting": "This is not the endpoint you are looking for!"}


# --- Get all posts:
@app.get("/posts")
def get_all_posts():
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    print(posts)
    return {"all_posts": posts}


# --- Get one post record based on its post_id (path parameter):
@app.get("/posts/{post_id}")
def get_one_post(post_id: int):
    print(type(post_id))
    for post in my_posts:
        if post["id"] == post_id:
            return {"post_data": post}
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"Post ID {post_id} not found")


# --- A post request that uses JSON from the Body of the request:
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def new_post(new_post: Post):
    
    # Create a new SQL query to write the record:
    cursor.execute("""INSERT INTO posts (title, content, published) 
                      VALUES (%s, %s, %s) 
                      RETURNING *;""",
                      (new_post.title, new_post.content, new_post.published))
    
    # --- Get the details of the new record and assign it to a variable:
    new_post = cursor.fetchone()
    
    # --- Commit the record to the table. Without this, the record will not be inserted into the table:
    conn.commit()
    
    # --- Return the value of the post:
    return {"status_code": status.HTTP_201_CREATED,
            "status_detail": "post has been created",
            "data": new_post
            }


@app.delete("/delete/{id}")
def delete_post(id: int):
    # index = find_index(id)
    
    # --- If record can't be found, raise a 404    
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post ID {id} not found")
    
    # Remove the index from the list:
    # my_posts.pop(index)
    print(f"{id}")
    try:
        cursor.execute("""DELETE FROM posts WHERE id = %s""",(id))
        conn.commit()
    except Exception as error:
                print("error getting data from table")    
                print(error)
        
    raise HTTPException(status_code = status.HTTP_200_OK)
  
   
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id = id)

    if index == None:
        # --- If record can't be found, raise a 404    
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"Post ID {id} not found")
    
    post_dict = post.dict()
    print(post_dict)
    post_dict["id"] = id
    my_posts[index] = post_dict
    
    raise HTTPException(status_code = status.HTTP_200_OK)





