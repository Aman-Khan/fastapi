from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class signUpInfo(BaseModel):
    email: EmailStr
    pwd: str

    class Config:
        orm_mode=True

class resSignUpInfo(BaseModel):
    id: int
    email: str
    acs: bool
    created_at: datetime
    
    class Config:
        orm_mode=True


class loginCred(BaseModel):
    email: EmailStr
    pwd: str
        
    class Config:
        orm_mode=True

class resToken(BaseModel):
    id: int
    token: str
        
    class Config:
        orm_mode=True

class userPost(BaseModel):
    id:Optional[int]
    context: str
    post: str
        
    class Config:
        orm_mode=True


class tokenData(BaseModel):
    id: str
    class Config:
        orm_mode = True