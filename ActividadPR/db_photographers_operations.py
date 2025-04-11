from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import Photographers

#adicionar un registro
async def db_add_photographer(db_session:AsyncSession, name:str, state:bool=None,):
    photographer = Photographers(name=name, state=state,)

    async with db_session.begin():
        db_session.add(photographer)
        await db_session.flush()
        photographer_id = photographer.id
        await db_session.commit()
    return photographer_id

#mostrar por id
async def db_show_one_photographer(photographer_id:int, db_session:AsyncSession):
    query = (select(Photographers).where(Photographers.id == photographer_id))
    result = await db_session.execute(query)

    photographer = result.scalars().first()

    return photographer

#mostrar todos los registros
async def db_show_all_photographers(db_session:AsyncSession): #db_session trae la base de datos
    query = (select(Photographers))
    result = await db_session.execute(query)
    photographers = result.scalars().all()

    return photographers

#modificar un registro
async def db_modify_state(photographer_id:int, actual_state:bool, db_session:AsyncSession):
    query = (update(Photographers).where(Photographers.id == photographer_id).values(name=actual_state))

    result = await db_session.execute(query)
    await db_session.commit() #confirma el cambio
    if result.rowcount == 0: #cuantas filas fueron modificadas
        return False
    return True

#eliminar registro
async def db_remove_photographer(photographer_id:int, db_session:AsyncSession):
    result = await db_session.execute(delete(Photographers).where(Photographers.id == photographer_id))
    await db_session.commit()
    if result.rowcount == 0: #si es igual a 0 no elimino nada
        return False
    return True