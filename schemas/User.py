from pydantic import BaseModel

class Session(BaseModel):
    Token: int
class Register(BaseModel):
    email: str
    username: str
    password: str
class Login(BaseModel):
    email: str
    password: str