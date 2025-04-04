from contextlib import asynccontextmanager
from os import getenv, path
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

DATABASE_URL = getenv('DOCKER_DATABASE_URL') if path.exists('/.dockerenv') else getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# fastapi async session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        except Exception as e:
            await session.rollback()
            raise e
        
# seed.py async session
@asynccontextmanager
async def get_session_seed() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        except Exception as e:
            await session.rollback()
            raise e
            