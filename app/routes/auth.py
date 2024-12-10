from app.utils import logger, hash_password, check_password
from fastapi.security import APIKeyHeader

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas import UserRegisterSchema

import uuid

router = APIRouter()
api_key_header = APIKeyHeader(name="Abraham-API-Key")

@router.post("/register")
def register_user(user: UserRegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    api_key = f"rag_{uuid.uuid4()}"
    new_user = User(name=user.name, email=user.email, hashed_password=hash_password(user.password), api_key=api_key)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"api_key": new_user.api_key}

@router.get("/verify")
def verify_api_key(api_key_header: str = Security(api_key_header),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.api_key == api_key_header).first()
    print(api_key_header)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"message": "API key is valid"}
