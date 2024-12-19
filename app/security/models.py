from pydantic import BaseModel
from app.models.user import User

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserInDB(User):
    hashed_password: str
    __allow_unmapped__ = True