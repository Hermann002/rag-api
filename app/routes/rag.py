from fastapi import APIRouter, Depends, UploadFile, Security, File, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
import uuid
from app.models.user import ApiKey, User
from sqlalchemy.exc import IntegrityError
from app.security.security import get_current_user, get_current_active_user
from typing import Annotated
from fastapi.security import APIKeyHeader

import os

router = APIRouter()
api_key_header = APIKeyHeader(name="Abraham-API-Key")

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

@router.post("/upload-docs/")
async def create_upload_file(file: UploadFile, api_key_header: str = Security(api_key_header),db: Session = Depends(get_db)):
    api_key = db.query(ApiKey).filter(ApiKey.api_key == api_key_header).first()
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    upload_dir = "app/uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    content = await file.read()
    with open(f"{upload_dir}/{file.filename}", "wb") as f:
        f.write(content)
    return {"filename": file.filename}

@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}