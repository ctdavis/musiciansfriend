from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from quotes_spider.items import QuotesSpiderItem

class QuotesSpider(Spider):
    name = 'quotes'

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            item = ItemLoader(QuotesSpiderItem())
            item.add_value('quote', quote.xpath('./span[@class="text"]/text()')\
                    .getall())
            item.add_value('author', quote.xpath('./span/small[@class="author"]/text()')\
                    .getall())
            yield item.load_item()
        next_page = response.xpath('//li[@class="next"]/a/@href')\
            .extract_first()
        #if next_page:
        #    yield Request(self.start_urls[0] + next_page)
