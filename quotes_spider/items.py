import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst

class QuotesSpiderItem(scrapy.Item):
    quote = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(output_processor=TakeFirst())
