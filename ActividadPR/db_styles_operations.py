from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import Styles

#adicionar un registro
async def db_add_style(db_session:AsyncSession, style_name:str):
    style = Styles(style_name=style_name,)

    async with db_session.begin():
        db_session.add(style)
        await db_session.flush()
        style_id = style.id
        await db_session.commit()
    return style_id

#mostrar por id
async def db_show_one_style(style_id:int, db_session:AsyncSession):
    query = (select(Styles).where(Styles.id == style_id))
    result = await db_session.execute(query)

    style = result.scalars().first()

    return style

#mostrar todos los registros
async def db_show_all_styles(db_session:AsyncSession): #db_session trae la base de datos
    query = (select(Styles))
    result = await db_session.execute(query)
    styles = result.scalars().all()

    return styles

#modificar un registro
async def db_modify_style(style_id:int, new_style:str, db_session:AsyncSession):
    query = (update(Styles).where(Styles.id == style_id).values(style_name=new_style:str))

    result = await db_session.execute(query)
    await db_session.commit() #confirma el cambio
    if result.rowcount == 0: #cuantas filas fueron modificadas
        return False
    return True

#eliminar registro
async def db_remove_style(style_id:int, db_session:AsyncSession):
    result = await db_session.execute(delete(Styles).where(Styles.id == style_id))
    await db_session.commit()
    if result.rowcount == 0: #si es igual a 0 no elimino nada
        return False
    return True