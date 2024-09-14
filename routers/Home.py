from fastapi import APIRouter, HTTPException, status, Depends
from ORMDatabases import db
from sqlalchemy import and_
from Server.Models.posts import posts
from middleware import get_current_user, IsModerator
from Server.Models.friends import LocalUser

app = APIRouter()

NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Not found")

@app.get("/", tags=["Main"])
def main(user=Depends(get_current_user)):
    try:
        if IsModerator(user.email) == True:
            list = db.query(posts).filter().all()
            return list
        list = db.query(posts).filter(posts.share == True).all()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return list
@app.get("/posts/{id}", tags=["Main"])
def list(id, user=Depends(get_current_user)):
    try:
        if IsModerator(user.email):
            list = db.query(posts).filter(and_(posts.id == int(id))).first()
            return list
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

@app.get("/users/{username}/friends", tags=["Main"])
def list(username):
    try:
        test = db.query(LocalUser).filter_by(username=username).first()
        friends = [friend.username for friend in test.friends]
    except Exception as e:
        raise e
    return {"Friends": friends}
@app.get("/users/{username}/posts", tags=["Main"])
def list(username, user=Depends(get_current_user)):
    try:
        if IsModerator(user.email):
            list = db.query(posts).filter(and_(posts.Creator == username)).all()
            return list
        list = db.query(posts).filter(and_(posts.Creator == username, posts.share == True)).all()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return list