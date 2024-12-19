import logging
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, security
from fastapi.security import HTTPBasic, HTTPBasicCredentials

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Configuration du logger
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

import hashlib

import bcrypt

def hash_password(password: str) -> str:
   hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
   return hashed_bytes.decode('utf-8')

# Usage example
def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user