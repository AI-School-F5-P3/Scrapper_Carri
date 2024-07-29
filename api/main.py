from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, Base, init_db
from typing import Optional
from logging_config import logger
import uvicorn
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

# Endpoints GET

@app.get("/autor/citas", tags = ['Autor'])
async def buscar_citas_autor_route(
    nombre_autor: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.buscar_citas_autor(db, nombre_autor)

@app.get("/autor/cita_random", tags = ['Autor'])
async def buscar_cita_aleatoria_autor_route(
    nombre_autor:str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.buscar_cita_aleatoria_autor(db, nombre_autor)

@app.get("/autor/about", tags = ['Autor'])
async def buscar_about_route(
    nombre_autor:str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.buscar_about(db, nombre_autor)

@app.get("/cita_dia")
async def buscar_cita_aleatoria_route(
    db: AsyncSession = Depends(get_db)
):
    return await crud.buscar_cita_aleatoria(db)

@app.get("/tags/cita", tags = ['Tags'])
async def buscar_citas_por_tags_route(
    tag1: str = None,
    tag2: Optional[str] = None,
    tag3: Optional[str] = None,
    tag4: Optional[str] = None,
    tag5: Optional[str] = None,
    tag6: Optional[str] = None,
    tag7: Optional[str] = None,
    tag8: Optional[str] = None,
    nombre_autor: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    tags = [tag for tag in [tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8] if tag]
    return await crud.buscar_citas_por_tags(db, tags, nombre_autor)

@app.get("/tags/list", tags = ['Tags'])
async def buscar_lista_citas_route(
    db:AsyncSession = Depends(get_db)
):
    return await crud.buscar_lista_citas(db)

if __name__ == "__main__":
    logger.info("incio de la aplicacion")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)