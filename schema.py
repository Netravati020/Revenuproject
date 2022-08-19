# from typing import Optional, List, UUID

from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class Revenue_t(BaseModel):

    branch:str
    target: float
    Ach: float
    Archp: float
    Archo: float
    clustername: str
    status: str

    class Config:
        orm_mode = True

class Adm_rev(BaseModel):

    unit: str
    total_net_revenue: int
    branch: str
    rdate: datetime
    date: datetime

    class Config:
        orm_mode = True

class Access(BaseModel):
    accesskey:str
    date: str

    class Config:
        orm_mode = True


class User(BaseModel):
    Name: str
    email:str
    password:str

class Login(BaseModel):
    username: str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Revenue_t):
    email: Optional[str] = None




