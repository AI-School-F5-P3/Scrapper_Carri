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

def insert_quotes_to_db():
    file_path = '/app/data/data_quotes.json'

    if not os.path.isfile(file_path):
        logger.error(f'El archivo no se encuentra: {file_path}')
        raise FileNotFoundError(f"El archivo no se encuentra: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)

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

        tag_ids = {}
        for quote in quotes_data:
            for tag in quote.get('tags', []):
                if tag not in tag_ids:
                    cur.execute(f"""
                        INSERT INTO {SCHEMA_NAME}.tag (tag)
                        VALUES (%s)
                        ON CONFLICT (tag) DO NOTHING
                        RETURNING id
                    """, (tag,))
                    tag_id = cur.fetchone()
                    if tag_id:
                        tag_ids[tag] = tag_id[0]

        author_ids = {}
        for quote in quotes_data:
            text = quote.get('quote')
            author_name = quote.get('author')
            if author_name not in author_ids:
                cur.execute(f"""
                    SELECT id FROM {SCHEMA_NAME}.author WHERE author = %s
                """, (author_name,))
                result = cur.fetchone()
                if result:
                    author_ids[author_name] = result[0]

            author_id = author_ids.get(author_name)

            if author_id:
                cur.execute(f"""
                    SELECT id FROM {SCHEMA_NAME}.quote
                    WHERE quote = %s AND author_id = %s
                """, (text, author_id))
                result = cur.fetchone()

                if result is None:
                    cur.execute(f"""
                        INSERT INTO {SCHEMA_NAME}.quote (quote, author_id)
                        VALUES (%s, %s)
                        RETURNING id
                    """, (text, author_id))
                    quote_id = cur.fetchone()[0]

                    for tag in quote.get('tags', []):
                        tag_id = tag_ids.get(tag)
                        if tag_id:
                            cur.execute(f"""
                                INSERT INTO {SCHEMA_NAME}.quote_tag (quote_id, tag_id)
                                VALUES (%s, %s)
                                ON CONFLICT DO NOTHING
                            """, (quote_id, tag_id))
                else:
                    quote_id = result[0]
                    for tag in quote.get('tags', []):
                        tag_id = tag_ids.get(tag)
                        if tag_id:
                            cur.execute(f"""
                                INSERT INTO {SCHEMA_NAME}.quote_tag (quote_id, tag_id)
                                VALUES (%s, %s)
                                ON CONFLICT DO NOTHING
                            """, (quote_id, tag_id))

        conn.commit()
        logger.info('Insertadas citas en la base de datos')
    except Exception as e:
        logger.error(f"Error al insertar datos en la base de datos: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        logger.info('Cerrada la conexión con la base de datos')

    os.remove(file_path)
    logger.info('Eliminado archivo JSON')

insert_quotes_to_db()
