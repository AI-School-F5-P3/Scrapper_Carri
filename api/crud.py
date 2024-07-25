from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from logger import logger
from typing import List
import random
import models


# Recuperar citas por autor

async def buscar_citas_autor(
    db:AsyncSession,
    nombre_autor: str
):
    result = await db.execute(
        select(models.Quote)
        .options(joinedload(models.Quote.author))
        .filter(models.Author.author == nombre_autor)
    )
    quotes = result.scalars().all()

    if not quotes:
        logger.error(f'{nombre_autor} no encontrado')
        raise HTTPException(status_code = 404, detail = "Autor no encontrado")
    
    quotes_data = {
        "nombre_autor": nombre_autor,
        "citas": [
            {"cita": quote.quote}
            for quote in quotes
        ]
    }

    logger.info(f'Recuperadas citas del autor {nombre_autor}')

    return quotes_data

# Recuperar cita random de autor

async def buscar_cita_aleatoria_autor(
    db: AsyncSession,
    nombre_autor: str
):
    result = await db.execute(
        select(models.Quote)
        .options(joinedload(models.Quote.author))
        .filter(models.Author.author == nombre_autor)
    )
    quotes = result.scalars().all()

    if not quotes:
        logger.error(f'{nombre_autor} no encontrado')
        raise HTTPException(status_code = 404, detail = "Autor no encontrado")
    
    random_quote = random.choice(quotes)

    random_quote_data = {
        "nombre_autor": nombre_autor,
        "citas": random_quote.quote
    }

    logger.info(f'Recuperada cita aleatoria de {nombre_autor}')

# Recuperar about de un autor

async def buscar_about(
    db: AsyncSession,
    nombre_autor: str
):
    result = await db.execute(
        select(models.Author)
        .filter(models.Author.author == nombre_autor)
    )
    author = result.scalars().first()

    if author is None:
        logger.error(f'{nombre_autor} no encontrado')
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    author_data = {
        "nombre_autor": nombre_autor,
        "about": author.about
    }

    logger.info(f'Recuperado "about" del autor {nombre_autor}')
    
    return author_data
                              

# Recuperar cita random en general

async def buscar_cita_aleatoria(
    db: AsyncSession,
):
    result = await db.execute(
        select(models.Quote)
    )
    quotes = result.scalars().all()

    if not quotes:
        logger.error(f'No hay citas disponibles')
        raise HTTPException(status_code = 404, detail = "No hay citas disponibles")
    
    random_quote = random.choice(quotes)

    random_quote_data = {
        "nombre_autor": random_quote.author.author,
        "citas": random_quote.quote
    }

    logger.info(f'Recuperada cita aleatoria')


async def buscar_citas_por_tags(
    db: AsyncSession,
    tags: List[str]
):
    # Verificar que se ha proporcionado al menos una etiqueta
    if not tags or len(tags) == 0:
        logger.error('Se debe proporcionar al menos una etiqueta')
        raise HTTPException(status_code=400, detail="Se debe proporcionar al menos una etiqueta")

    # Limitar el número de etiquetas a 8
    if len(tags) > 8:
        logger.error('Se pueden proporcionar un máximo de 8 etiquetas')
        raise HTTPException(status_code=400, detail="Se pueden proporcionar un máximo de 8 etiquetas")

    # Construir la consulta para filtrar las citas que contengan todas las etiquetas proporcionadas
    tag_subqueries = []
    for tag in tags:
        tag_subqueries.append(
            select(models.Quote.id)
            .join(models.quote_tag_table)
            .join(models.Tag)
            .filter(models.Tag.tag == tag)
            .subquery()
        )

    if not tag_subqueries:
        logger.error('No se encontraron citas con las etiquetas proporcionadas')
        raise HTTPException(status_code=404, detail="No se encontraron citas con las etiquetas proporcionadas")

    # Usar un join en las subconsultas para obtener las citas que coincidan con todas las etiquetas
    query = select(models.Quote).filter(
        models.Quote.id.in_(tag_subqueries[0])
    )
    for subquery in tag_subqueries[1:]:
        query = query.filter(
            models.Quote.id.in_(subquery)
        )

    result = await db.execute(query)
    quotes = result.scalars().all()

    if not quotes:
        logger.error('No se encontraron citas con las etiquetas proporcionadas')
        raise HTTPException(status_code=404, detail="No se encontraron citas con las etiquetas proporcionadas")
    
    # Formatear la respuesta para incluir las citas con las etiquetas específicas
    quotes_data = {
        "etiquetas": tags,
        "citas": [
            {
                "cita": quote.quote,
                "autor": quote.author.author,
                "tags": [tag.tag for tag in quote.tags]
            }
            for quote in quotes
        ]
    }

    logger.info(f'Recuperadas citas con las etiquetas {tags}')
    
    return quotes_data