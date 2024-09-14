import os
from fastapi import APIRouter, Depends, HTTPException, status, Response
from schemas.User import Login
from utils.AuthToken import CreateEncodedToken
from validators.userValidators import CheckUserLogin
from typing import Annotated
from ORMDatabases import db
from middleware import get_current_user2
from schemas.posts import Title

from Server.Models.posts import posts
from Server.Models.Moderator import Moderator
from Server.Models.User import User

app = APIRouter()

NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Not found")

UPLOAD_FOLDER = 'Static/Uploaded'

@app.post("/Moderators/login", tags=["Moderator"])
def login(data: Annotated[Login, Depends(CheckUserLogin)], response: Response):
    try:
        email = data.get("email")
        ServerEmail = db.query(Moderator).filter(Moderator.email == email).first()
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
            detail="Incorrect email or password",
        )

@app.delete("/Moderators/posts", tags=["Moderator"])
def delete(id, user=Depends(get_current_user2)):
    try:
        list = db.query(posts).filter(posts.id == id).first()
        db.delete(list)
        db.commit()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return {f" {user.email} Deteled": id}

@app.delete("/Moderators/posts", tags=["Moderator"])
def delete(id, user=Depends(get_current_user2)):
    try:
        list = db.query(posts).filter(posts.id == id).first()
        db.delete(list)
        db.commit()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return {f" {user.email} Deteled": id}

@app.get("/Moderators/all/files/list", tags=["Moderator"])
def list_all_files():
    all_files = {}

    for user_folder in os.listdir(UPLOAD_FOLDER):
        user_folder_path = os.path.join(UPLOAD_FOLDER, user_folder)

        if os.path.isdir(user_folder_path):
            user_files = os.listdir(user_folder_path)
            all_files[user_folder] = user_files

    return {"All Users' Uploaded Files": all_files}

@app.get("/Moderators/all/files/list", tags=["Moderator"])
def list_all_files():
    all_files = {}

    for user_folder in os.listdir(UPLOAD_FOLDER):
        user_folder_path = os.path.join(UPLOAD_FOLDER, user_folder)

        if os.path.isdir(user_folder_path):
            user_files = os.listdir(user_folder_path)
            all_files[user_folder] = user_files

    return {"All Users' Uploaded Files": all_files}

@app.put("/posts/{id}", tags=["Moderator"])
def update(id, data: Title):
    try:
        newpost = db.query(posts).filter(posts.id == int(id)).first()
        if newpost == None:
            raise NotFound
        newpost.title = data.title
        newpost.content = data.content
        newpost.share = data.share
        newpost.friendonly = data.friendonly
        db.commit()
    except Exception as e:
        raise NotFound
    return {"Detail": "Post updated successfully"}

@app.delete("/Moderators/all/files/delete", tags=["Moderator"])
def delete_file(email: str, filename: str):
    user_folder_path = os.path.join(UPLOAD_FOLDER, email)
    if not filename.endswith('.png'):
        filename = filename + ".png"
    if not os.path.exists(user_folder_path):
        return {"error": f"Folder for user {email} does not exist."}

    file_path = os.path.join(user_folder_path, filename)
    if not os.path.exists(file_path):
        return {"error": f"File '{filename}' not found for user {email}."}
    os.remove(file_path)

    return {"message": f"File '{filename}' successfully deleted for user {email}."}

# @app.delete("/Moderators/users/delete/{email}", tags=["Moderator"])
# def remove_user(email):
#     try:
#
#         ServerEmail = db.query(User).filter(User.email == email).first()
#         db.delete(ServerEmail)
#         db.commit()
#     except Exception:
#         raise NotFound
#     return {"message": f"Sucessfullly delete {ServerEmail.email}"}