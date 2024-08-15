from pydantic import BaseModel
from typing import Optional
class Title(BaseModel):
    title: str
    content: str
    public: Optional[bool] = None
    friendonly: Optional[bool] = None