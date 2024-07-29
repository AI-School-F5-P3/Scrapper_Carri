import scrapy
from logging_config import logger

class QuotegetterSpider(scrapy.Spider):
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
