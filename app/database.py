import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

load_dotenv()

# # Function to check if we are inside a docker container
# def is_running_in_docker() -> bool:
#     return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

# Determine DATABASE_URL
DATABASE_URL = os.getenv('DOCKER_DATABASE_URL') if os.path.exists('/.dockerenv') else os.getenv('DATABASE_URL')

# SQLAlchemy setup for async
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# FastAPI async session
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
        
# Seed.py async session
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
        