from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# --- Create a constant that will be used to point to and pass the user details to our database:
SQLALCHEMY_DATABASE_URL = "postgresql://neil:password@localhost/fastapi"


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