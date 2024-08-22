from fastapi import APIRouter, Depends, HTTPException, status
from middleware import get_current_user
from Server.Models.friends import LocalUser
from ORMDatabases import db

app = APIRouter()

NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Not found")


@app.post("/add_friend/{friend_username}")
def add_friend(friend_username: str, user=Depends(get_current_user)):
    try:
        you = db.query(LocalUser).filter(LocalUser.username == user.username).first()
        if not you:
            db.add(LocalUser(username=user.username))
            db.commit()
            you = db.query(LocalUser).filter(LocalUser.username == user.username).first()
        friend = db.query(LocalUser).filter(LocalUser.username == friend_username).first()
        if not friend:
            db.add(LocalUser(username=friend_username))
            db.commit()
            friend = db.query(LocalUser).filter(LocalUser.username == friend_username).first()

        if not user or not friend:
            raise NotFound

        you.friends.append(friend)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return {"msg": f"{friend_username} added as a friend to {you}"}