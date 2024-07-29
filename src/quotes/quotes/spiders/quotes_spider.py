import scrapy
from logging_config import logger

class QuotegetterSpider(scrapy.Spider):
    '''
    Clase que define el comportamiento de la araña de citas.
    Se definen custom_settings para guardar los resultados en un json en una carpeta concreta para luego utilizarla en la inserción de datos a la base de datos.
    start_request comienza el proceso de scrap con la URL de la página.
    parse define el proceso de scrap.
    '''
    name = "quotes"

    custom_settings = {
        'FEEDS': {
            '/app/data/data_quotes.json': {
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
        Se especifica donde se deben extraer los datos en el código html fuente de la página. Para acceder a ello se requiere de usar una herramiento tipo "inspeccionar elemento" o "inspeccionar codigo fuente" en el navegador que se esté utilizando (Brave, Firefox, Chrome...)
        Se incluye además una función para continuar scrapeando en la siguiente página de la web, si existe.
        '''
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            text = text.replace("â€œ", '"').replace("â€", '"').replace("â€™", "'")
            
            author = quote.css('span small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            logger.info('Extraidos datos de cita')

            yield {
                'quote': text,
                'author': author,
                'tags': tags
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            logger.info('Siguiente página')
            yield response.follow(next_page, self.parse)
