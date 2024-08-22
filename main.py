from fastapi import FastAPI
from routers import users, files, posts, Home, addfriend

app = FastAPI()

app.include_router(users.app, prefix="/api/v1")
app.include_router(users.app, prefix="/api/v1")
app.include_router(files.app, prefix="/api/v1")
app.include_router(posts.app, prefix="/api/v1")
app.include_router(addfriend.app, prefix="/api/v1")
app.include_router(Home.app, prefix="")