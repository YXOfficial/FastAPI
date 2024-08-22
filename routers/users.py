from ORMDatabases import db
from utils.AuthToken import CreateEncodedToken, CreateRefreshToken
from fastapi import APIRouter, HTTPException, Depends, Response, status
from schemas.User import Register, Login
from validators.userValidators import CheckUserRegister, validate_password, CheckUserLogin
from middleware import get_current_user
from typing import Annotated
from Server.Models.User import User

app = APIRouter()


@app.post("/user/register")
def Register(data: Annotated[Register, Depends(CheckUserRegister)]):
    try:
        validate_password(data.get("password"))
        NewUser = User(email=data.get('email'), username=data.get('username'), password=data.get('password'))
        db.add(NewUser)
        db.commit()
        return {"message": "Created Account."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@app.post("/user/login")
def login(data: Annotated[Login, Depends(CheckUserLogin)], response: Response):
    try:
        email = data.get("email")
        ServerEmail = db.query(User).filter(User.email == email).first()
        if data.get("password") == ServerEmail.password:
            if not ServerEmail.Token:
                access_token = CreateEncodedToken(data)
                ServerEmail.Token = access_token
                db.commit()
                response.set_cookie(key="access_token", value=access_token, httponly=True)
                return {"access_token": access_token, "token_type": "bearer"}
            else:
                access_token = ServerEmail.Token
                # RefreshToken = CreateRefreshToken(data)
                response.set_cookie(key="access_token", value=access_token, httponly=True)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"Message": "Incorrect password."})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get("/users/me")
def home(user=Depends(get_current_user)):
        return {"Hello": user.username}

@app.get("/logout")
def logout(response: Response):
        return response.delete_cookie("access_token")