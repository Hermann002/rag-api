from pydantic import BaseModel, EmailStr, constr

class UserRegisterSchema(BaseModel):
    username: constr(min_length=1, strip_whitespace=True)
    email: EmailStr
    password: constr(min_length=8)

class UserLoginSchema(BaseModel):
    username : constr(min_length=1, strip_whitespace=True)
    password : constr(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
