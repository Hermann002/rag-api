from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
import uuid
from app.models.user import ApiKey, User
from sqlalchemy.exc import IntegrityError
from app.security.security import get_current_user, get_current_active_user
from typing import Annotated

router = APIRouter()

@router.get("/create-api-key")
def create_api_key(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    api_key = f"rag_{uuid.uuid4()}"
    api_db = db.query(ApiKey).filter(ApiKey.api_key==api_key).first()
    if api_db:
        raise IntegrityError("Something went wrong !")
    
    new_api_key = ApiKey(api_key=api_key, owner_id=current_user.id)
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)
    return {"new_api_key": new_api_key}