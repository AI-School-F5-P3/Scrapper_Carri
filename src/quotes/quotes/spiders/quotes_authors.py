import scrapy
import html
from logging_config import logger

class AuthorsSpider(scrapy.Spider):
    '''
    Clase que define el comportamiento de la araña de autores.
    Se definen custom_settings para guardar los resultados en un json en una carpeta concreta para luego utilizarla en la inserción de datos a la base de datos.
    start_request comienza el proceso de scrap con la URL de la página.
    parse define el proceso de scrap, se incluye una flag para verificar si se están encontrando autores en la búsqueda.
    '''
    name = "authors"

    custom_settings = {
        'FEEDS': {
            '/app/data/data_authors.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
    }

    def start_requests(self):
        URL = 'https://quotes.toscrape.com/'
        yield scrapy.Request(url=URL, callback=self.parse)

    def parse(self, response):
        '''
        Se buscan las urls para los auotres especificando donde se encuentran en el código html fuente de la página. Para acceder a ello se requiere de usar una herramiento tipo "inspeccionar elemento" o "inspeccionar codigo fuente" en el navegador que se esté utilizando (Brave, Firefox, Chrome...)
        Se incluye además una función para continuar scrapeando en la siguiente página de la web, si existe.
        '''
        found_authors = False  # Bandera para verificar si se encontraron autores
        for quote in response.css('div.quote'):
            author = quote.css('span small.author::text').get()
            author_link = quote.css('span a::attr(href)').get()
            if author and author_link:
                found_authors = True
                author_about_url = response.urljoin(author_link)
                
                # Hacer una solicitud para obtener la biografía del autor
                request = scrapy.Request(author_about_url, callback=self.parse_author_about)
                request.meta['author_name'] = author
                yield request
                logger.info('Encontrado autor')
            else:
                logger.error('No se encuentra autor: %s')

        # Si no se encontraron autores, registra un error
        if not found_authors:
            logger.error('No se encuentra URL de autor en página %s')

        # Seguir a la siguiente página si existe
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            logger.info('Siguiente página')
            yield response.follow(next_page, self.parse)

    def parse_author_about(self, response):
        # Extraer la biografía del autor
        description = response.css('div.author-description::text').get()
        description = html.unescape(description) if description else 'No description available'

        yield {
            'author': response.meta['author_name'],
            'about': description.strip(),
        }
