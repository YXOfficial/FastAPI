from ORMDatabases import db
from fastapi import Request
from utils import AuthToken
from fastapi import HTTPException, status
from Server.Models.User import User
from Server.Models.Moderator import Moderator
def get_current_user(request: Request):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        access_token = request.cookies.get("access_token")
        users = AuthToken.DecodeToken(access_token)
        email = users.get('email')
        ServerEmail = db.query(User).filter(User.email == email).first()
    except Exception as e:
        raise token_exception
    return ServerEmail

def IsModerator(email):
    Test = db.query(Moderator).filter(Moderator.email == email).first()
    if Test:
        return True
    else:
        return False

def get_current_user2(request: Request):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        access_token = request.cookies.get("access_token")
        users = AuthToken.DecodeToken(access_token)
        email = users.get('email')
        ServerEmail = db.query(Moderator).filter(Moderator.email == email).first()
    except Exception as e:
        raise token_exception
    return ServerEmail