from app.database import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import null, text


# --- Create a class for a post that is an extension of Base from the database.py file:
class Post(Base):
    # --- ___tablename___ tells SQLAlchemy which table to use for this model.
    # --- If the table named "posts" is not found, it will create it.
    # --- If this wasn't set, the name of the table would be the name of the class in lowercase:
    __tablename__ = "posts"
    
    # --- Define the columns for this model:
    id         = Column(Integer, primary_key = True, nullable = False)
    title      = Column(String, nullable = False)
    content    = Column(String, nullable = False)
    published  = Column(Boolean, server_default = "TRUE", nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text("now()"))
    owner_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    

# --- Create a class for a user that is an extension of Base from the database.py file:
class User(Base):
    # --- specify the table name to use.
    __tablename__ = "users"
    
    # --- Define the columns for this model:
    id         = Column(Integer, primary_key = True, nullable = False)
    email      = Column(String, nullable = False, unique = True)
    password   = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text("now()"))