from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

DATA_BASE_URL = ("sqlite+aiosqlite:///photographersdb.db")

def get_engine():
    return create_async_engine(DATA_BASE_URL, echo=True)

AsyncSessionLocal = sessionmaker (autoflush = False, autocommit = False, bind = get_engine(), class_ = AsyncSession)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session