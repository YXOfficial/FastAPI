from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from schemas.User import Register, Login
from ORMDatabases import db
from Server.Models.User import User
def CheckUserRegister(RegisterRequest: Register):
    data = jsonable_encoder(RegisterRequest)
    ServerEmail = db.query(User).filter(User.email == data.get('email')).first()
    if ServerEmail:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail={"Message": "Already exists"})
    return data

def CheckUserLogin(LoginRequest: Login):
    data = jsonable_encoder(LoginRequest)
    ServerEmail = db.query(User).filter(User.email == data.get('email')).first()
    if not ServerEmail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"Message": "Invalid email"})
    return data
def validate_password(value):
        if len(value) > 40:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"Message": "Password too long"})
        elif len(value) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"Message": "Password too short"})