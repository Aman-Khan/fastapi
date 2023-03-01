from fastapi import FastAPI
from .router import auth, post 
from pydantic import BaseSettings

setting = BaseSettings()
app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)