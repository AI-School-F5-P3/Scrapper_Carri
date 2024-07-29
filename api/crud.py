from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from fastapi import HTTPException
from typing import List
from logging_config import logger
import random
import models



# Recuperar citas por autor

async def buscar_citas_autor(
    db:AsyncSession,
    nombre_autor: str
):
    # Query para seleccionar en la table Quote, uniendola con la tabla Autor, aquellas entradas que coincidan con el nombre del autor que el usuario define.
    result = await db.execute(
        select(models.Quote)
        .options(joinedload(models.Quote.author))
        .filter(models.Author.author == nombre_autor)
    )
    quotes = result.scalars().all() # Se extraen todas las entradas de la tabla

    if not quotes:
        logger.error(f'{nombre_autor} no encontrado')
        raise HTTPException(status_code = 404, detail = "Autor no encontrado")
    
    # Modelo de respuesta
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
    # Query para seleccionar en la table Quote, uniendola con la tabla Autor, aquellas entradas que coincidan con el nombre del autor que el usuario define.
    result = await db.execute(
        select(models.Quote)
        .options(joinedload(models.Quote.author))
        .filter(models.Author.author == nombre_autor)
    )
    quotes = result.scalars().all() # Se extraen todas las entradas de la tabla

    if not quotes:
        logger.error(f'{nombre_autor} no encontrado')
        raise HTTPException(status_code = 404, detail = "Autor no encontrado")
    
    random_quote = random.choice(quotes) # Se extraen una cita aleatoria del resultado previo

    # Modelo de respuesta
    random_quote_data = {
        "nombre_autor": nombre_autor,
        "citas": random_quote.quote
    }

    logger.info(f'Recuperada cita aleatoria de {nombre_autor}')

    return random_quote_data

# Recuperar about de un autor

async def buscar_about(
    db: AsyncSession,
    nombre_autor: str
):
    # Query para seleccionar en la tabla Autor,aquellas entradas que coincidan con el nombre del autor que el usuario define.
    result = await db.execute(
        select(models.Author)
        .filter(models.Author.author == nombre_autor)
    )
    author = result.scalars().first() # Se recupera el primer resultado

    if author is None:
        logger.error(f'{nombre_autor} no encontrado')
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    # Modelo de respuesta
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
    try:
        # Ejecutar la consulta para obtener todas las citas, cargando la relación del autor para poder luego imprimir cita y su autor
        result = await db.execute(
            select(models.Quote).options(
                joinedload(models.Quote.author)
            )
        )
        quotes = result.scalars().all()

        if not quotes:
            logger.error('No hay citas disponibles')
            raise HTTPException(status_code=404, detail="No hay citas disponibles")
        
        random_quote = random.choice(quotes) # Elegir una cita aleatoria

        # Modelo de respuesta
        random_quote_data = {
            "nombre_autor": random_quote.author.author if random_quote.author else "Desconocido",
            "cita": random_quote.quote
        }

        logger.info('Recuperada cita aleatoria')

        return random_quote_data

    except Exception as e:
        logger.error(f'Error al recuperar la cita aleatoria: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")

async def buscar_citas_por_tags(
    db: AsyncSession,
    tags: List[str],
    nombre_autor: str
):
    # Verificar que se ha proporcionado al menos una etiqueta
    if not tags:
        logger.error('Se debe proporcionar al menos una etiqueta')
        raise HTTPException(status_code=400, detail="Se debe proporcionar al menos una etiqueta")

    # Limitar el número de etiquetas a 8 ya que es el número máximo que aparece en quotes.toscrape.com
    if len(tags) > 8:
        logger.error('Se pueden proporcionar un máximo de 8 etiquetas')
        raise HTTPException(status_code=400, detail="Se pueden proporcionar un máximo de 8 etiquetas")

    # Query para filtrar las citas que contengan todas las etiquetas proporcionadas
    tag_subqueries = []
    for tag in tags:
        # Se selecciona la tabla Quote y se une a la tabla intermedia quote_tag, que se une a la tabla tag y filtra donde coincidan las etiquetas con las que ha introducido el usuario
        subquery = (
            select(models.Quote.id)
            .join(models.quote_tag_table)
            .join(models.Tag)
            .filter(models.Tag.tag == tag)
            .subquery()
        )
        tag_subqueries.append(subquery)

    # Si no hay subconsultas, se lanzará una excepción, pero esto no debería suceder ya que se verifica antes
    if not tag_subqueries:
        logger.error('No se encontraron citas con las etiquetas proporcionadas')
        raise HTTPException(status_code=404, detail="No se encontraron citas con las etiquetas proporcionadas")

    # Usar un join en las subconsultas para obtener las citas que coincidan con TODAS las etiquetas
    query = select(models.Quote).options(selectinload(models.Quote.author)).filter(
        models.Quote.id.in_(tag_subqueries[0])
    )
    for subquery in tag_subqueries[1:]:
        query = query.filter(
            models.Quote.id.in_(subquery)
        )

    if nombre_autor:
        # Obtener el ID del autor
        author_subquery = (
            select(models.Author.id)
            .filter(models.Author.author == nombre_autor)
            .subquery()
        )
        # Modificar la consulta para incluir el filtro por autor
        query = query.join(models.Author).filter(
            models.Author.id.in_(author_subquery)
        )

    result = await db.execute(query)
    quotes = result.scalars().all()

    if not quotes:
        logger.error('No se encontraron citas con las etiquetas proporcionadas')
        raise HTTPException(status_code=404, detail="No se encontraron citas con las etiquetas proporcionadas")

    # Modelo de respuesta
    quotes_data = [
        {
            "nombre_autor": quote.author.author,  
            "cita": quote.quote
        }
        for quote in quotes
    ]

    logger.info(f'Recuperadas citas con las etiquetas {tags}')
    
    return quotes_data

async def buscar_lista_citas(
    db: AsyncSession
)-> List[str]:
    # Construir la consulta para obtener todas las etiquetas únicas
    query = select(models.Tag.tag).distinct()

    try:
        result = await db.execute(query)
        tags = result.scalars().all()
        
        logger.info('Recuperadas todas las etiquetas únicas')
        return tags
    
    except Exception as e:
        logger.error(f'Error al recuperar las etiquetas: {e}')
        raise HTTPException(status_code=500, detail="Error al recuperar las etiquetas")
    

async def buscar_palabra_clave(
    palabra: str,
    db: AsyncSession
):
    if not palabra.strip():
        logger.error('Se debe proporcionar una palabra clave válida')
        raise HTTPException(status_code=400, detail="Se debe proporcionar una palabra clave válida")
    
    # Query para buscar citas que contengan la palabra clave en la tabla Quote
    query = (
        select(models.Quote)
        .options(selectinload(models.Quote.author))
        .filter(models.Quote.quote.ilike(f'%{palabra}%')) # Este regex busca la palabra que el usuario incluya en el texto de la cita. Esto incluye palabras que contengan la palabra clave, por ejemplo si la palabra es 'love', si una cita incluye 'lover' también devuelve dicha cita
    )
    
    result = await db.execute(query)
    quotes = result.scalars().all()
    
    # Verificar si se encontraron citas
    if not quotes:
        logger.info('No se encontraron citas con la palabra clave proporcionada')
        raise HTTPException(status_code=404, detail="No se encontraron citas con la palabra clave proporcionada")
    
    # Modelo de respuesta
    quotes_data = [
        {
            "nombre_autor": quote.author.author,  # Dado que author no puede ser None
            "cita": quote.quote
        }
        for quote in quotes
    ]
    
    logger.info(f'Recuperadas citas que contienen la palabra clave "{palabra}"')
    
    return quotes_data