from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import api
from app.core.config import settings
from app.db import init_db


@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa
    await init_db.init()
    yield


app = FastAPI(title="CertMS", lifespan=lifespan, debug=settings.DEBUG)

app.include_router(api.router)


@app.get("/")
def root():
    return {"Hello": "World"}
