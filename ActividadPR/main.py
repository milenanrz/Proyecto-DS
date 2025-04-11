from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.testing.plugin.plugin_base import engines
from starlette.responses import JSONResponse

import models
from models import *
from operations import *
from typing import List
from contextlib import asynccontextmanager
from database import Base
from db_connection import AsyncSessionLocal, get_db_session, get_engine
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from db_operations import *


@asynccontextmanager
async def lifespan(app:FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello Photographers"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request,exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message":"Algo falló",
            "detail":exc.detail,
            "path":request.url.path
        },
    )

@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)

@app.post("/dbphotographer", response_model=dict[str, bool])
async def add_photographer(photographer:Photographer, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    photographer_id = await db_add_photographer(db_session, photographer.name, photographer.state,)
    return {"New photographer":photographer_id}

@app.get("/dbphotographer/{photographer_id}", response_model=PhotographerWithId)
async def show_photographer_db(photographer_id:int, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    photographer = await db_show_one(photographer_id = photographer_id, db_session = db_session)
    if photographer is None:
        raise HTTPException(status_code=404, detail="No photographers in the database")
    return photographer

@app.get("/dball", response_model=list[PhotographerWithId])
async def show_all_photographer_db(db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    photographers =await db_show_all(db_session=db_session)
    if photographers is None:
        raise HTTPException(status_code=404, detail="Photographers not found")
    return photographers

@app.put("/dbpet/{photographer_id}")
async def update_pet_db(db_session:Annotated[AsyncSession,Depends(get_db_session)], photographer_id:int, actual_state:bool):
    photographer = await db_modify_state(photographer_id=photographer_id, actual_state=actual_state, db_session=db_session)
    return photographer

@app.delete("/dbphotographer/{photographer_id}")
async def delete_photographer_db(photographer_id:int, db_session:Annotated[AsyncSession,Depends(get_db_session)]):
    result = await db_remove(photographer_id=photographer_id, db_session=db_session)
    return result
