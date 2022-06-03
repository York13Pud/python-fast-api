from app.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql.expression import null


# --- Create a class for a post that is an extension of Base from the database.py file:
class Post(Base):
    # --- ___tablename___ tells SQLAlchemy which table to use for this model:
    __tablename__ = "posts"
    
    # --- Define the columns for this model:
    id        = Column(Integer, primary_key = True, nullable = False)
    title     = Column(String, nullable = False)
    content   = Column(String, nullable = False)
    published = Column(Boolean, default = True)
    
