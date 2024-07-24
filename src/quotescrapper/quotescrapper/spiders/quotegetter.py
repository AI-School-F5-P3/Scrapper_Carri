import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher


class QuotegetterSpider(scrapy.Spider):
    name = "quotegetter"

    def start_requests(self):
        URL = 'https://quotes.toscrape.com'
        yield scrapy.Request(url=URL, callback = self.response_parser)

    def response_parser(self, response):
        for selector in response.css('div.quote'):
            yield{
                'text': selector.css('span.text::text').get(),
                'author': selector.css('span small.author::text').get(),
                'tags': selector.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.response_parser)


def quotes_books_result():
    quotes_results = []

    def crawler_results(item):
        quotes_results.append(item)

    dispatcher.connect(crawler_results, signal = signals.item_scraped)
    crawler_process = CrawlerProcess(settings={
        'FEEDS': {
            'quotes_data.csv': {
                'format': 'csv', 
                'overwrite': True
            }
        }
    })
    crawler_process.crawl(QuotegetterSpider)
    crawler_process.start()
    return quotes_results

if __name__ == '__main__':
    quotes_data = quotes_books_result()

    keys = quotes_data[0].keys()
    with open('quotes_data.csv', 'w', newline = '', encoding='utf-8') as output_file_name:
        writer = csv.DictWriter(output_file_name, keys, delimiter = ';')
        writer.writeheader()
        writer.writerows(quotes_data)

    