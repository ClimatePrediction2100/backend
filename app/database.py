from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DB_URL)

Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        await db.close()
