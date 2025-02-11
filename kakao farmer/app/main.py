from fastapi import FastAPI
from app.database.connec_db import *
from app.routers import *

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(users.router)
app.include_router(videos.router)
app.include_router(formations.router)
