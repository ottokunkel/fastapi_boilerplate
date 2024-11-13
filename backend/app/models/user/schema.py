from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    refresh_token: Optional[str] = None