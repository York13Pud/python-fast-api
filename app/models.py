from app.database import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import null, text


# --- Create a class for a post that is an extension of Base from the database.py file:
class Post(Base):
    # --- ___tablename___ tells SQLAlchemy which table to use for this model.
    # --- If the table named "posts" is not found, it will create it:
    __tablename__ = "posts"
    
    # --- Define the columns for this model:
    id         = Column(Integer, primary_key = True, nullable = False)
    title      = Column(String, nullable = False)
    content    = Column(String, nullable = False)
    published  = Column(Boolean, server_default = "TRUE", nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text("now()"))
    
