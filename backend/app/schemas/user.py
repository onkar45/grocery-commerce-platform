from pydantic import BaseModel, EmailStr

class AdminCreateRequest(BaseModel):
    email: EmailStr
    password: str
    role: str  # admin or staff

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
