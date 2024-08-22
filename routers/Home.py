from fastapi import APIRouter, HTTPException, status, Depends
from ORMDatabases import db
from sqlalchemy import and_
from Server.Models.posts import posts
from middleware import get_current_user
from Server.Models.friends import LocalUser

app = APIRouter()

NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Not found")

@app.get("/")
def main():
    try:
        list = db.query(posts).filter(posts.share == True).all()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return list
@app.get("/posts/{id}")
def list(id, user=Depends(get_current_user)):
    try:
        userpermission = db.query(posts).filter(and_(posts.id == int(id), posts.email == user.email, posts.share == False)).first()
        if userpermission:
            list = db.query(posts).filter(and_(posts.id == int(id))).first()
            return {"Warning private posts": list}
        list = db.query(posts).filter(and_(posts.id == int(id), posts.share == True)).first()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return list

@app.get("/users/{username}/friends")
def list(username):
    try:
        list = db.query(LocalUser).filter(and_(LocalUser.username == username)).first()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return {"Friends": list.friends}
@app.get("/users/{username}/posts")
def list(username):
    try:
        list = db.query(posts).filter(and_(posts.Creator == username, posts.share == True)).all()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return list