from fastapi import FastAPI
from routers import users, files, posts, Home, friends, Moderator

app = FastAPI(
    title="My Custom API",
    description="This is a detailed description of my API.",
    version="2.0.0"
)

app.include_router(users.app, prefix="/api/v1")
app.include_router(users.app, prefix="/api/v1")
app.include_router(files.app, prefix="/api/v1")
app.include_router(posts.app, prefix="/api/v1")
app.include_router(friends.app, prefix="/api/v1")
app.include_router(Moderator.app, prefix="/api/v1")
app.include_router(Home.app, prefix="")
