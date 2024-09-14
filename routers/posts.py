from fastapi import APIRouter, Depends, HTTPException, status
from middleware import get_current_user
from schemas.posts import Title
from ORMDatabases import db
from Server.Models.posts import posts

app = APIRouter()

NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Not found")

@app.post("/posts", tags=["user"])
def create(data: Title, user=Depends(get_current_user)):
    newpost = posts(Creator=user.username, title=data.title, content=data.content, email=user.email, share=data.share, friendonly=data.friendonly)
    db.add(newpost)
    db.commit()
    return {"Detail": "Post created successfully"}

@app.get("/posts", tags=["user"])
def list(user=Depends(get_current_user)):
    try:
        list = db.query(posts).filter(posts.email == user.email).all()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return list

@app.delete("/posts/{id}", tags=["user"])
def delete(id, user=Depends(get_current_user)):
    try:
        list = db.query(posts).filter(posts.id == id and posts.email == user.email).first()
        db.delete(list)
        db.commit()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return {"Deteled": id}

@app.put("/posts/{id}", tags=["user"])
def update(id, data: Title, user=Depends(get_current_user)):
    try:
        newpost = db.query(posts).filter(posts.id == int(id) and posts.email == user.email).first()
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