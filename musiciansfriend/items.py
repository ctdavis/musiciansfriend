# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader.processors import MapCompose,TakeFirst
import re

def clean_price(price):
    return re.sub(r'(\$|,)','',price)

class MusiciansfriendItem(Item):
    url = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(str.strip, clean_price), output_processor=TakeFirst())
    name = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    brand = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    availability = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    style = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
