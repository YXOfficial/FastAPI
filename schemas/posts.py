from pydantic import BaseModel
from typing import Optional
class Title(BaseModel):
    title: str
    content: str
    share: Optional[bool] = None
    friendonly: Optional[bool] = None