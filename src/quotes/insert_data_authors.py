import json
import psycopg2
import os
from dotenv import load_dotenv
from logging_config import logger

# Cargar variables de entorno

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
SCHEMA_NAME = os.getenv("DB_SCHEMA")

def insert_authors_to_db():
    file_path = '/app/data/data_authors.json'

    if not os.path.isfile(file_path):
        logger.error(f'El archivo no se encuentra: {file_path}')
        raise FileNotFoundError(f"El archivo no se encuentra: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        authors_data = json.load(f)

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        logger.info('Abierta la conexión con la base de datos')

        author_ids = {}
        for author in authors_data:
            author_name = author.get('author')
            about = author.get('about', '').strip()
            if author_name and author_name not in author_ids:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}.author (author, about)
                    VALUES (%s, %s)
                    ON CONFLICT (author) DO UPDATE
                    SET about = EXCLUDED.about
                    RETURNING id
                """, (author_name, about))
                author_id = cur.fetchone()
                if author_id:
                    author_ids[author_name] = author_id[0]
                else:
                    logger.error(f'No puede recuperarse el ID de: {author_name}')
                    raise Exception(f"No puede recuperarse el ID de: {author_name}")

        conn.commit()
        logger.info('Insertados autores en la base de datos')
    except Exception as e:
        logger.error(f"Error al insertar datos en la base de datos: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        logger.info('Cerrada la conexión con la base de datos')

    os.remove(file_path)
    logger.info('Eliminado archivo JSON')

insert_authors_to_db()


