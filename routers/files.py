from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from typing import Annotated
from middleware import get_current_user
import os
import shutil

app = APIRouter()
UPLOAD_FOLDER = 'Static/Uploaded'

@app.post("/files/upload")
def upload(filename: str = Annotated[bytes | None, File()], Image: UploadFile = File(...), user=Depends(get_current_user)):
    email = user.email
    NewUploadFolder = os.path.join(UPLOAD_FOLDER, email)
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

        return {"filename": filename, "Saved at:": file_location}

    OriginalFilename = Image.filename
    file_location = os.path.join(NewUploadFolder, OriginalFilename)
    if Image.filename.endswith('.png'):
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(Image.file, file_object)
    else:
        return {'Invalid file format'}

    return {"filename": OriginalFilename, "Saved at:": file_location}

@app.get("/files/list")
def list(user=Depends(get_current_user)):
    email = user.email
    NewUploadFolder = os.path.join(UPLOAD_FOLDER, email)
    if not os.path.exists(NewUploadFolder):
        os.mkdir(NewUploadFolder)
    List = os.listdir(NewUploadFolder)

    return {"Uploaded Files": List}

@app.get("/files/download")
def download(user=Depends(get_current_user), filename: str = Annotated[bytes | None, File()]):
    email = user.email
    try:
        if not filename.endswith('.png'):
            filename = filename + ".png"
    except:
        return {"Not found"}
    DownloadFile = os.path.join(UPLOAD_FOLDER, email, filename)
    return FileResponse(path=DownloadFile, filename=filename)