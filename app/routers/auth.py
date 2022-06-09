from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(tags = ["Authentication"])

@router.post("/login")
def login(db: Session = Depends(get_db)):
    pass