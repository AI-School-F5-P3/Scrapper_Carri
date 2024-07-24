import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

class QuotegetterSpider(scrapy.Spider):
    name = "quotegetter"

    def start_requests(self):
        URL = 'https://quotes.toscrape.com/'
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
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

def quotes_books_result():
    quotes_results = []

    def crawler_results(item):
        quotes_results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(QuotegetterSpider)
    crawler_process.start()
    return quotes_results

def expand_tags(quotes_data):
    expanded_data = []
    for quote in quotes_data:
        base = {k: v for k, v in quote.items() if k != 'tags'}
        for i, tag in enumerate(quote['tags']):
            base[f'tag_{i+1}'] = tag
        expanded_data.append(base)
    return expanded_data

if __name__ == '__main__':
    quotes_data = quotes_books_result()
    expanded_data = expand_tags(quotes_data)
    
    keys = set()
    for quote in expanded_data:
        keys.update(quote.keys())
    keys = list(keys)

    with open('quotes_data.csv', 'w', newline='', encoding='utf-8') as output_file_name:
        writer = csv.DictWriter(output_file_name, fieldnames=keys, delimiter=';')
        writer.writeheader()
        writer.writerows(expanded_data)