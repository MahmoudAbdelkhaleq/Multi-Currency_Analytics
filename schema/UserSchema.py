from typing import List

from pydantic import BaseModel
from .InvoiceSchema import Invoice

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserCreate):
    pass

class User(UserBase):
    id: int
    is_active: bool
    # invoices: List[Invoice] = []

    class Config:
        orm_mode = True