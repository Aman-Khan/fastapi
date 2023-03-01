from fastapi import FastAPI
from .router import auth, post, get, patch, delete, like
from pydantic import BaseSettings

setting = BaseSettings()
app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(get.router)
app.include_router(patch.router)
app.include_router(delete.router)
app.include_router(like.router)