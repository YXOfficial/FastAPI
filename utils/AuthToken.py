import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
import os
from core.database import checkToken
import random
from os import environ
os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = "1"
reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)
SECRET_KEY = "1"



def CreateEncodedToken(data):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
# def GetCurrentUser(token):
#     payload = DecodeToken(token)
#     email = payload.get('gmail')
#     if not email:
#         raise 404
#     user = getuser(payload)
#     if not checkUser(user):
#         raise 404
#     return user

def CreateRefreshToken(data):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
def DecodeToken(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    print(payload)
    return payload

# e = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnbWFpbCI6InRoZTY2Nmtob2FAZ21haWwuY29tIiwicGFzc3dvcmQiOiJ0ZXN0In0.AmXUmd8Wca-6SlC0KFXW5uDwGHDMPscXBwRQ8H4QQFI"
# GetCurrentUser(e)