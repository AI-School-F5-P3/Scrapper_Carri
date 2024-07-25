from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, Base, init_db
from logger import logger
import uvicorn
import schemas
import crud
import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    logger.error('Excecpión no recogida', exc_info = (exc_type, exc_value, exc_traceback))
sys.exceptohook = handle_exception

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()


descripcion_API = '''
La API de frases celebres permite a los usuarios acceder a diferentes frases acuñadas por ilustres autores de la historia mundial, puediendo elegirse en función del autor, o de una serie de 'tags' según el ánimo personal del usuario.
'''

tags_metadata = [
    {
        "name": "Autor",
        "descripcion": "Operaciones con el autor de referencia",
    },
    {
        "name": "Tags",
        "descripción": "Operaciones con los tags de referencia"
    }
]

app = FastAPI(
    title = 'Base de datos de citas celebres',
    description = descripcion_API,
    summary = 'API para extraer citas de la base de datos',
    version = '0.0.0.0.1',
    terms_of_service = 'cuidao',
    openapi_tags = tags_metadata,
    lifespan = lifespan
)

async def get_db():
    async with SessionLocal() as session:
        yield session


async def on_startup():
    await init_db()

app.add_event_handler("startup", on_startup)