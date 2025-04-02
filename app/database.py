from contextlib import asynccontextmanager
from dotenv import load_dotenv
from os import getenv, path
from typing import AsyncGenerator

load_dotenv()

def is_demo_mode() -> bool:
    return getenv('DEMO_MODE', 'false').lower() == 'true'

if is_demo_mode():
    from boto3 import resource

    def get_dynamo_table():
        dynamodb = resource('dynamodb', region_name='us-east-2')
        return dynamodb.Table('codescript-problems')

    get_session = None
    get_session_seed = None
else:
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

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
    
    get_dynamo_table = None
            