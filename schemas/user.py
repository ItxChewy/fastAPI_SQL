from typing import Optional
from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str]
    username: str
    name: str
    password: str
    weight: float
    date: date

