from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.testing.plugin.plugin_base import engines
from starlette.responses import JSONResponse
from typing import Optional
from models import *
from contextlib import asynccontextmanager
from database import Base
from photographers_operations import *
from photographers_connection import AsyncSessionLocal, get_photographers_session, get_engine
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from styles_operations import *
from styles_connection import AsyncSessionLocal, get_styles_session, get_engine


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


@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)

#endpoints to photographers CRUD

@app.post("/photographer", response_model=dict[str, bool])
async def add_photographer(photographer:Photographer, db_session:Annotated[AsyncSession,Depends(get_photographers_session)]):
    photographer_id = await add_photographer(db_session, photographer.name, photographer.state,)
    return {"New photographer":photographer_id}

@app.get("/photographer/{photographer_id}", response_model=PhotographerWithId)
async def show_photographer(photographer_id:int, db_session:Annotated[AsyncSession,Depends(get_photographers_session)]):
    photographer = await show_one_photographer(photographer_id = photographer_id, db_session = db_session)
    if photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return photographer

@app.get("/all_photographers", response_model=list[PhotographerWithId])
async def show_all_photographer(db_session:Annotated[AsyncSession,Depends(get_photographers_session)]):
    photographers =await show_all_photographers(db_session=db_session)
    if photographers is None:
        raise HTTPException(status_code=404, detail="Photographers not found")
    return photographers

@app.put("/photographer/{photographer_id}")
async def update_photographer(db_session:Annotated[AsyncSession,Depends(get_photographers_session)], photographer_id:int, actual_state:bool):
    photographer = await modify_state(photographer_id=photographer_id, actual_state=actual_state, db_session=db_session)
    if photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return photographer

@app.delete("/photographer/{photographer_id}")
async def delete_photographer(photographer_id:int, db_session:Annotated[AsyncSession,Depends(get_photographers_session)]):
    result = await remove_photographer(photographer_id=photographer_id, db_session=db_session)
    if result is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return result

@app.get("/photographer_filter/{photographer_state}", response_model=list[PhotographerWithId])
async def state_filter (photographer_state:bool, db_session:Annotated[AsyncSession,Depends(get_photographers_session)]):
    photographer = await filter_state_photographer(photographer_state=photographer_state, db_session=db_session)
    if photographer is None:
        raise HTTPException(status_code=404, detail="No photographers in the database")
    return photographer


#endpoints to photografic styles CRUD

@app.post("/photographic_style", response_model=dict[str, str])
async def add_styles(style:PhotographicStyle, db_session:Annotated[AsyncSession,Depends(get_styles_session)]):
    style_id = await add_style(db_session, style.name, style.style_name,)
    return {"New style":style_id}

@app.get("/photographic_style/{style_id}", response_model=StyleWithId)
async def show_style(style_id:int, db_session:Annotated[AsyncSession,Depends(get_styles_session)]):
    style = await show_one_style(style_id = style_id, db_session = db_session)
    if style is None:
        raise HTTPException(status_code=404, detail="Photographic style not found")
    return style

@app.get("/all_photographic_styles", response_model=list[StyleWithId])
async def show_all_styles_(db_session:Annotated[AsyncSession,Depends(get_styles_session)]):
    styles =await show_all_styles(db_session=db_session)
    if styles is None:
        raise HTTPException(status_code=404, detail="Photographic styles not found")
    return styles

@app.put("/photographic_style/{style_id}")
async def update_style(db_session:Annotated[AsyncSession,Depends(get_styles_session)], style_id:int, new_style:str):
    style = await modify_style(style_id=style_id, new_style=new_style, db_session=db_session)
    if style is None:
        raise HTTPException(status_code=404, detail="Photographic style not found")
    return style

@app.delete("/photographic_style/{style_id}")
async def delete_style(style_id:int, db_session:Annotated[AsyncSession,Depends(get_styles_session)]):
    result = await remove_style(style_id=style_id, db_session=db_session)
    if result is None:
        raise HTTPException(status_code=404, detail="Photographic style not found")
    return result

@app.get("/find_style/{style_name_}", response_model=list[StyleWithId])
async def find_styles(style_name_:str, db_session:Annotated[AsyncSession,Depends(get_styles_session)]):
    style = await find_style(style_name_ = style_name_, db_session = db_session)
    if style is None:
        raise HTTPException(status_code=404, detail="No photographic styles in the database")
    return style

@app.exception_handler(HTTPException)
async def http_exception_handler(request,exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message":"Error!",
            "detail":exc.detail,
            "path":request.url.path
        },
    )