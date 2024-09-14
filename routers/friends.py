from fastapi import APIRouter, Depends, HTTPException, status
from middleware import get_current_user
from Server.Models.friends import LocalUser, friendship_table
from ORMDatabases import db
from schemas.friends import FriendRequestAccept
import json
app = APIRouter()

NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Not found")


@app.post("/add_friend/{friend_username}", tags=["user"])
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

        you.sent_requests.append(friend)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return {"msg": f"{you} sent friend request to {friend_username}"}

@app.post("/friend-requests", tags=["user"])
def friend_requests(user=Depends(get_current_user)):
    try:
        you = db.query(LocalUser).filter(LocalUser.username == user.username).first()
        list = you.sent_requests
        # incoming_requests = session.query(LocalUser).join(
        #     friendship_table,
        #     (friendship_table.c.user_id == LocalUser.id)
        # ).filter(
        #     friendship_table.c.friend_id == user.id,
        #     friendship_table.c.status == 'pending'
        # ).all()
        incoming_requests = db.query(LocalUser).join(friendship_table, LocalUser.id == friendship_table.c.user_id).filter_by(
            friend_id=you.id,
            status='pending'
        ).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return {"Pending": list,
            "Incoming Requests": incoming_requests}

@app.post("/friend-requests/VerifyRequest", tags=["user"])
def VerifyRequest(data: FriendRequestAccept, user=Depends(get_current_user)):
    try:
        you = db.query(LocalUser).filter(LocalUser.username == user.username).first()
        friend = db.query(LocalUser).filter(LocalUser.username == data.username).first()
        request = db.query(friendship_table).filter_by(user_id=friend.id, friend_id=you.id, status='pending').first()
        if request and data.status == True:
            db.execute(friendship_table.update().where(friendship_table.c.user_id == friend.id, friendship_table.c.friend_id == you.id).values(status='accepted'))
            you.friends.append(friend)
            db.commit()
            db.execute(friendship_table.update().where(
                friendship_table.c.user_id == you.id, friendship_table.c.friend_id == friend.id).values(
                status='accepted'))
            db.commit()
        else:
            db.execute(friendship_table.delete().where(friendship_table.c.user_id == friend.id, friendship_table.c.friend_id == you.id))
            return {"Rejected": data.username}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return {"Added": data.username}

@app.post("/friend-requests/unfriend/{friend_username}", tags=["user"])
def unfriend(friend_username: str, user=Depends(get_current_user)):
    try:
        # you = db.query(LocalUser).filter(LocalUser.username == user.username).first()
        # friend = db.query(LocalUser).filter(LocalUser.username == friend_username).first()
        # db.execute(friendship_table.delete().where(friendship_table.c.user_id == friend.id,
        #                                            friendship_table.c.friend_id == you.id).values(status='accepted'))
        # db.execute(friendship_table.delete().where(friendship_table.c.user_id == you.id,
        #                                            friendship_table.c.friend_id == friend.id).values(status='accepted'))
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return {"Unfriended": friend_username}