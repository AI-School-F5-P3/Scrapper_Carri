import psycopg2
import os
import scrapy
import html
import time
import schedule
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from dotenv import load_dotenv
from logging_config import logger


#Base de datos
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

SCHEMA_NAME = 'quotes'


class QuotegetterSpider(scrapy.Spider):
    '''
    Esta clase va a definir la 'spider' que va a recorrer la página de quotes para extraer los datos de texto, autor y etiquetas asociadas, necesita un nombre por si cremaos más arañas poder gestionarlas en los archivos creados por el proyecto de scrapy
    '''
    name = "quotegetter"

    def start_requests(self):
        '''
        Start_requests es el método de la araña que define la url de la página que queremos scrapear
        '''
        URL = 'https://quotes.toscrape.com/'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        '''
        response_parser es el método de la araña que define que partes van a extraerse de la página, y que nombre vamos a asociar a esas variables.
        selector in response.css toma como argumento la clase donde van a encontrarse todos los datos que necesitamos scrapear, en nuestro caso se encuentran en div quote, que se puede encontrar mediante la función inspeccionar elemento en nuestro navegador de referencia (Firefox, Chrome, Brave, etc.). 
        Una vez definido el response.css, indicamos que apartados de ese response (marcado como selector en nuestro bucle) queremos extraer, de nuevo hay que utilizar inspeccionar elemento para determinar cuales son los apartados, en nuestro caso por ejemplo, el texto se encuentra dentro de <span, class = "text"> por lo que pasamos como argumento span.text::text, los dos puntos indican que el elemento que queremos extraer es text.

        En el caso del texto de la cita, se ha añadido además un text.replace ya que la codificación de la web provoca que algunos símbolos como las comillas dobles y simples se codifiquen mal, en este caso de momento se ha añadido manualmente los elementos érroneos para que se sustituyan por el carácter correcto, pero es un método no recomendable.

        yield devuelve el formato estilo JSON en el que queremos devolver el contenido que se ha scrapeado.

        Por último se añade una funcionalidad para que el scraper visite todas las páginas de la web, indicando en que punto está el hipervinculo a la siguiente página, y de existir, seguir extrayendo las citas.
        '''
        for selector in response.css('div.quote'):
            text = selector.css('span.text::text').get()
            text = text.replace("â€œ", '"').replace("â€", '"').replace("â€™", "'")
            
            author = selector.css('span small.author::text').get()
            author_link = selector.css('span small.author ~ a::attr(href)').get()
            tags = selector.css('div.tags a.tag::text').getall()
            
            author_about_url = response.urljoin(author_link)

            request = scrapy.Request(author_about_url, callback=self.parse_author_about)
            request.meta['quote_text'] = text
            request.meta['author_name'] = author
            request.meta['tags'] = tags
            yield request
            logger.info(f'Extraido ítem con spider {request}')

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.response_parser)
            logger.info('Cambio de página')

    def parse_author_about(self, response):
        '''
        Este método se genera para poder extraer los "about" de los autores para luego guardarlos en la base de datos
        '''
        description = response.css('div.author-description::text').get()
        description = html.unescape(description)

        print(f"Extracted about: {description}")

        yield {
            'quote': response.meta['quote_text'],
            'author': response.meta['author_name'],
            'about': description,
            'tags': response.meta['tags']
        }

def quotes_spider_result():
    '''
    Esta función servirá para comenzar el proceso de scrap e ir guardando los resultados que se encuentre nuestra spider.
    dispatcher.connect ejecuta la función crawler_results() cuando la araña encuentra un ítem objetivo (crawler_results añade el ítem a los resultados)
    crawler_process.crawl asocia el proceso a la spider que hemos creado previamente.
    crawler.process.start() inicia la ejecución, cuando se complete el scrap de un ítem objetivo hará una llamada (signal) item_scraped, que como se ha mencionado antes, provoca que se ejecute la función crawler_results y se añada el ítem a los resultados.
    Cuando se finaliza el proceso se devuelven los resultados scrapeados.
    '''
    quotes_results = []

    def crawler_results(item):
        quotes_results.append(item)
        logger.info('Guardado resultado')

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(QuotegetterSpider)
    crawler_process.start()
    return quotes_results

def insert_data_to_db(quotes_data):
    '''
    Esta función permitirá introducir los datos que se extraigan de la página en la base de datos que hayamos creado previamente.
    Primero se debe realizar la conexión a la base de datos, para ello se ha utilizado un archivo de variables de entorno .env para aumentar la seguridad, cada usuario tendrá que crearse el suyo con los datos pertinentes.

    A continuación, con los datos extraidos por la spider, se irán incluyendo los datos extraidos a las tablas que queramos y en función de las columnas que hayamos definido.
    '''
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host='quotes-db',
        port=5432
    )
    cur = conn.cursor()

    '''
    Para insertar los datos en la tabla de autores, se necesita recorrer todos los datos que se han extraido en quotes_data, de aquí se extrae el nombre del autor y el "about" correspondiente.
    En author_ids se iran guardando los autores que ya se hayan añadido en la base de datos, para que solo se inserten en la base de datos una vez.
    cur.execute es una función de psycopg2 que permite realizar ejecuciones sql en python, en este caso cuando encontramos un autor que no está en la base de datos se inserta en la tabla autor su nombre y su "about". Si hay un conflicto en autor se actualiza el "about".
    Despues se comprueba con cur.fetchone y el siguiente condicional que la ejecución ha sido correcta, en cuyo caso se guarda en el diccionario author_ids el id del autor que se acaba de insertar.
    Si el proceso falla, dentro del else se incluye una segunda comproboción que busca el id del autor en función del nombre que ha obtenido al scrapear el item. De esta forma se valida una segunda vez si existe el autor para evitar errores.
    Por último, si de esta forma tampoco se localiza un id se genera una excepción (error) para avisar al usuario de que no se encuentra el autor en la base de datos.

    Este proceso se repite para los tags y para las citas. Para las citas además se van a guardar en diferentes columnas todas las etiquetas posibles que presente una cita.

    Por último se ejecutan las acciones en la base de datos y se cierra el cursos y la conexión a la base de datos.
    '''
    author_ids = {}
    for quote in quotes_data:
        author = quote['author']
        about = quote.get('about', '').strip() # strip elimina los espacios en blanco antes del texto
        if author not in author_ids:
            cur.execute(f"""
                INSERT INTO {SCHEMA_NAME}.author (author, about)
                VALUES (%s, %s)
                ON CONFLICT (author) DO UPDATE
                SET about = EXCLUDED.about
                RETURNING id
            """, (author, about))
            author_id = cur.fetchone()
            if author_id:
                author_ids[author] = author_id[0]
                logger.info(f'Añadido {author} correctamente')
            else:
                # Si falla la inserción se busca el id por nombre del autor.
                cur.execute(f"SELECT id FROM {SCHEMA_NAME}.author WHERE author = %s", (author,))
                author_id = cur.fetchone()
                if author_id:
                    author_ids[author] = author_id[0]
                    logger.info(f'Añadido {author} correctamente')
                else:
                    logger.error(f'No puede recuperarse el ID de: {author}')
                    raise Exception(f"No puede recuperarse el ID de: {author}")
                    

    # Tags e ids
    tag_ids = {}
    for quote in quotes_data:
        for tag in quote['tags']:
            if tag not in tag_ids:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}.tag (tag)
                    VALUES (%s)
                    ON CONFLICT (tag) DO NOTHING
                    RETURNING id
                """, (tag,))
                tag_id = cur.fetchone()
                if tag_id:
                    logger.info(f'Añadidas tags correctamente')
                    tag_ids[tag] = tag_id[0]
                else:
                    cur.execute(f"SELECT id FROM {SCHEMA_NAME}.tag WHERE tag = %s", (tag,))
                    tag_id = cur.fetchone()
                    if tag_id:
                        tag_ids[tag] = tag_id[0]
                        logger.info(f'Añadidas tags correctamente')
                    else:
                        logger.error(f'No puede recuperarse el ID de: {tag}')
                        raise Exception(f"No puede recuperarse el ID de: {tag}")

    # Insert quotes
    for quote in quotes_data:
        text = quote['quote']
        author_id = author_ids[quote['author']]

        cur.execute(f"""
            INSERT INTO {SCHEMA_NAME}.quote (quote, author_id)
            VALUES (%s, %s)
            RETURNING id
        """, (text, author_id))
        quote_id = cur.fetchone()[0]

        for tag in quote['tags']:
            tag_id = tag_ids[tag]
            cur.execute(f"""
                INSERT INTO {SCHEMA_NAME}.quote_tag (quote_id, tag_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (quote_id, tag_id))

    conn.commit()
    logger.info('Commit realizado correctamete')
    cur.close()
    conn.close()
    logger.info('Cerrada la conexion a la base de datos')

def funcion_base():
    logger.info('Inicio de scraping y actualización de db')
    quotes_data = quotes_spider_result()
    insert_data_to_db(quotes_data)
    logger.info('Scraping y actualización de la base de datos completada')

def job():
    '''
    Funcion para introducir en el gestor de tiempos, para ejecutar el programa cada 12 horas
    '''
    funcion_base()

if __name__ == '__main__':
    logger.info('Inicio del programa')
    funcion_base() # Hacer una primera ejecución al correr el script
    logger.info('Comienza la espera de 12 horas')
    schedule.every(12).hours.do(job) # Ejecutar después cada 12 horas

    while True:
        schedule.run_pending()
        time.sleep(1)