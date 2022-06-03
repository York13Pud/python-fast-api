from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor

# --- Create a constant that will be used to point to and pass the user details to our database:
SQLALCHEMY_DATABASE_URL = "postgresql://neil:password@localhost/fastapi"

# --- Create an engine to connect to the database:
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# --- Create a session to the database:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Define the base:
Base = declarative_base()