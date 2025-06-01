from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    
class CreateUser(UserBase):
    password: str
    
class UserResponse(UserBase):
    createdAt: datetime
    id: int
    model_config = {
        'from_attributes': True
    }
    
class UserLogin(UserBase):
    password: str
    