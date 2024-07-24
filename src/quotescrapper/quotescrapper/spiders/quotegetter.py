import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

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
            tags = selector.css('div.tags a.tag::text').getall()
            
            yield {
                'text': text,
                'author': author,
                'tags': tags,
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.response_parser)

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

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(QuotegetterSpider)
    crawler_process.start()
    return quotes_results

def expand_tags(quotes_data):
    '''
    La función expand_tags sirve para en lugar de devolver una lista con todas las tags asociada a una cita, nos devuelve cada cita por separado para poder incorporarla al archivo de datos.
    '''
    expanded_data = []
    for quote in quotes_data:
        base = {k: v for k, v in quote.items() if k != 'tags'}
        for i, tag in enumerate(quote['tags']):
            base[f'tag_{i+1}'] = tag
        expanded_data.append(base)
    return expanded_data

if __name__ == '__main__':
    '''
    La función de inicio ejecuta la función de scrapeo y la función de expansión de las tags.
    Después crea un csv donde se almacenan todos los datos que se han scrapeado, el siguiente paso será añadirlos a una base de datos postgres.
    '''
    quotes_data = quotes_spider_result()
    expanded_data = expand_tags(quotes_data)
    
    # Determine the maximum number of tags
    max_tags = max(len(quote['tags']) for quote in quotes_data)
    keys = ['text', 'author'] + [f'tag_{i+1}' for i in range(max_tags)]

    with open('quotes_data.csv', 'w', newline='', encoding='utf-8') as output_file_name:
        writer = csv.DictWriter(output_file_name, fieldnames=keys, delimiter=';')
        writer.writeheader()
        writer.writerows(expanded_data)