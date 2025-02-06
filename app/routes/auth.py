from app.utils import logger
from app.security.security import get_password_hash, get_current_active_user, authenticate_user, create_access_token
from fastapi.security import APIKeyHeader
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User, ApiKey, OneTimePasscode
from app.schemas import UserRegisterSchema, UserLoginSchema, UserResponse, OTPSchema
from typing import Annotated
from app.security.models import Token
from app.config import settings
from app.utils import send_code_email, send_normal_mail
from app.security.security import get_current_user

db = get_db()

router = APIRouter()
api_key_header = APIKeyHeader(name="Abraham-API-Key")

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserRegisterSchema, db: Session = Depends(get_db)):
    check_username = db.query(User).filter(User.username == user.username).first()
    if check_username:
        raise HTTPException(status_code=400, detail="Username already exist !")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered !")
    
    new_user = User(username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(new_user) 
    db.commit()

    await send_code_email(user.email, db)
    return new_user

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token: # headers : Content-Type: application/x-www-form-urlencoded
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# @router.get("/verify")
# def verify_user(api_key_header: str = Security(api_key_header),db: Session = Depends(get_db)):
#     api_key = db.query(ApiKey).filter(ApiKey.api_key == api_key_header).first()
#     print(api_key_header)
#     if not api_key:
#         raise HTTPException(status_code=401, detail="Invalid API key")
#     return {"message": "API key is valid"}

@router.post("/verify-user", response_model=UserResponse)
def verify_user(otp: OTPSchema, db: Session=Depends(get_db)):
    verify_otp = db.query(OneTimePasscode).filter(OneTimePasscode.code == otp.otp).first()
    if verify_otp:
        user = verify_otp.owner
        user.is_active = True
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Not found !")
    return user

# headers = {
#         "Authorization": f"Bearer {token}"
#     }

@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user