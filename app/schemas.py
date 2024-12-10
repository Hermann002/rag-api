from pydantic import BaseModel, EmailStr, constr

class UserRegisterSchema(BaseModel):
    name: constr(min_length=1, strip_whitespace=True)
    email: EmailStr
    password: constr(min_length=8)