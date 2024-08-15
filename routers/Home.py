from fastapi import APIRouter, HTTPException, status
from ORMDatabases import db
from Server.Models.posts import posts

app = APIRouter()

NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Not found")

@app.get("/")
def main():
    try:
        list = db.query(posts).filter(posts.public == "1").all()
        if list == None:
            raise NotFound
    except Exception as e:
        raise NotFound
    return list