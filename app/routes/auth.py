from app.utils import logger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User

import uuid

router = APIRouter()

@router.post("/register")
def register_user(name: str, email: str, hashed_password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    api_key = f"rag_{uuid.uuid4()}"
    new_user = User(name=name, email=email, hashed_password=hashed_password, api_key=api_key)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"api_key": new_user.api_key}

@router.get("/verify")
def verify_api_key(api_key: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"message": "API key is valid"}
