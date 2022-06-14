from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# --- Create a constant that will be used to point to and pass the user details to our database:
SQLALCHEMY_DATABASE_URL = f"{settings.database_type}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


# --- Create an engine to connect to the database:
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# --- Create a session to the database:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Define the base that can be used with other callable classes, such as a class to make a Table:
Base = declarative_base()


# --- Execute the connection to the database and close it when finished:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
# --- Old psycopg2 connection method:

# --- Setup the connection to the database:
# connection_successful = False
# query_successful = False


# --- Attempt to connect to the database:
# while connection_successful is False:
#     try:
#         # --- Setup the connection:
#         conn = psycopg2.connect(host="localhost", 
#                                 dbname="fastapi", 
#                                 user="postgres", 
#                                 password="",
#                                 cursor_factory=RealDictCursor
#                                 )
        
#         # --- Create a cursor to allow execution of commands:
#         cursor = conn.cursor()
#         print("Connected to DB")
        
#         # --- Set connection_successful to True to stop the loop:
#         connection_successful = True
        
#         # --- Attempt to get the records in the database:
#         while query_successful is False:
#             try:
#                 cursor.execute("SELECT * FROM posts;")
#                 print(cursor.fetchone())
#                 query_successful = True
                
#             # --- Display an error if the query fails:    
#             except Exception as error:
#                 print("error getting data from table")    
#                 print(error)
#                 sleep(5)
                
#     # --- Display an error if the connection fails:            
#     except Exception as error:
#         print("error connecting to DB")
#         print(error)
#         sleep(5)