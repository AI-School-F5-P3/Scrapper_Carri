from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text
import os
from dotenv import main

main.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

Base = declarative_base()

db_type = os.getenv('DB_TYPE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_schema = os.getenv('DB_SCHEMA')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')

database_url = f'{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

SQLALCHEMY_DB = database_url

engine = create_async_engine(SQLALCHEMY_DB, echo = True)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine, class_= AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        try:
            await conn.execute(text(f'SET seatch_path to {db_schema}'))
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            raise
    
async def shutdown_db():
    await SessionLocal.close()
