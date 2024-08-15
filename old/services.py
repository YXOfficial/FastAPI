import datetime


from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from core import database
from core.database import getuser, checkUser, CreateUser, CreateToken, checkToken
from utils.AuthToken import CreateEncodedToken, DecodeToken, reusable_oauth2, CreateRefreshToken
from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Response, Request
from fastapi.responses import FileResponse
from typing import Annotated
import shutil
import os
app = APIRouter()
UPLOAD_FOLDER = 'Static/Uploaded'
cursor = database.cursor
utcnow = int(datetime.datetime.now().timestamp())
class Session(BaseModel):
    Token: int
class register(BaseModel):
    gmail: str
    username: str
    password: str

class TokenBase(BaseModel):
    token_type: str
    token: str

class login(BaseModel):
    gmail: str
    password: str

@app.post("/register/")
def Register(RegisterRequest: register):
        data = jsonable_encoder(RegisterRequest)
        gmail = data.get('gmail')
        account = getuser(gmail)
        if checkUser(account):
            return {"message": "Already exists."}
        else:
            CreateUser(data)
            access_token = CreateEncodedToken(data)
            CreateToken(access_token, gmail)
            return {"message": "Created Account."}

@app.post("/login")
def login(LoginRequest: login, response: Response, request: Request):
    data = jsonable_encoder(LoginRequest)
    gmail = data.get('gmail')
    account = getuser(gmail)
    accountutc = int(account['account'][6].timestamp())
    if checkUser(account) and data.get("password") == account['account'][2]:
        if not account['account'][5]:
            access_token = CreateEncodedToken(data)
            CreateToken(access_token, gmail)
        else:
            access_token = account['account'][5]
            RefreshToken = CreateRefreshToken(data)
            response.set_cookie(key="token", value=RefreshToken, httponly=True)
            # responses.set_cookie(key="token", value=access_token)
            # GetCurrentUser(access_token)
        return TokenBase(token=RefreshToken, token_type='Bearer')
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.post("/UploadImage/", dependencies=[Depends(reusable_oauth2)])
def UploadImage(filename: str = Annotated[bytes | None, File()], Image: UploadFile = File(...), user: Session=Depends(reusable_oauth2)):
    Token = checkToken(user.credentials)
    if not Token:
        return {}
    user = Token[3]
    NewUploadFolder = os.path.join(UPLOAD_FOLDER, user)
    if not os.path.exists(NewUploadFolder):
        os.mkdir(NewUploadFolder)
    if filename:
        if not filename.endswith('.png'):
            filename = filename + ".png"
        file_location = os.path.join(NewUploadFolder, filename)
        if Image.filename.endswith('.png'):
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(Image.file, file_object)
        else:
            return {'Invalid file format'}
        # shutil.copy2(Image.file, UploadPath)
        return {"filename": filename, "Saved at:": file_location}

    OriginalFilename = Image.filename
    file_location = os.path.join(NewUploadFolder, OriginalFilename)
    if Image.filename.endswith('.png'):
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(Image.file, file_object)
    else:
        return {'Invalid file format'}
    # shutil.copy2(Image.file, UploadPath)
    return {"filename": OriginalFilename, "Saved at:": file_location}

@app.get("/uploadedfile", dependencies=[Depends(reusable_oauth2)])
def uploaded_file(user: Session=Depends(reusable_oauth2)):
    Token = checkToken(user.credentials)
    if not Token:
        return {}
    user = Token[3]
    NewUploadFolder = os.path.join(UPLOAD_FOLDER, user)
    if not os.path.exists(NewUploadFolder):
        os.mkdir(NewUploadFolder)
    List = os.listdir(NewUploadFolder)
    # if not GetCurrentUser(token):
    #     return {}

    return {"Uploaded Files": List}

@app.get("/downloadfile", dependencies=[Depends(reusable_oauth2)])
def Download(filename: str = Annotated[bytes | None, File()], user: Session=Depends(reusable_oauth2)):
    Token = checkToken(user.credentials)
    if not Token:
        return {}
    user = Token[3]
    try:
        if not filename.endswith('.png'):
            filename = filename + ".png"
    except:
        return {"Not found"}

    DownloadFile = os.path.join(UPLOAD_FOLDER, user, filename)

    return FileResponse(path=DownloadFile, filename=filename)

@app.get("/users/me", dependencies=[Depends(reusable_oauth2)])
def home(user: Session=Depends(reusable_oauth2)):
    user = checkToken(user.credentials)
    if not user:
        return {}
    else:
        return {"Hello": user[1]}