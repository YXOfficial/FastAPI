from pydantic import BaseModel
from typing import Optional
class FriendRequestAccept(BaseModel):
    username: str
    status: Optional[bool] = None