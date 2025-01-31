from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import settings

DATABASE_URL = f'postgresql+asyncpg://{settings.db.DB_USER}:{settings.db.DB_PASS}@{settings.db.DB_HOST}:{settings.db.DB_PORT}/{settings.db.DB_NAME}'

database = Database(DATABASE_URL)

engine = create_async_engine(DATABASE_URL) # движок для обращения к БД из питона
async_session_maker = async_sessionmaker(engine, expire_on_commit=False) # Фабрика сессий

async def get__async_session():
    async with async_session_maker() as session:
        yield session

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __allow_unmapped__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"