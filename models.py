from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password_hash: str
    ssn: str
    active: int = 1

class CartItem(BaseModel):
    price: float
    quantity: int

class UserSearch(BaseModel):
    username: str