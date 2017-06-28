from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from musiciansfriend.items import MusiciansfriendItem
from urllib.parse import urljoin, urldefrag, urlparse
import logging

class MusiciansFriend(Spider):
    name = 'musiciansfriend'
    start_urls = ['http://www.musiciansfriend.com']
    main_menu_xpath = '//ul[@class="navDeptList"]/li/a/@href'
    sub_menu_xpath = '//div[@class="cat-list-cap"]/a/@href'
    product_listing_xpath = '//div[@class="product"]/div[2]/strong/a/@href'
    product_xpath = '//dl[@id="styleSelect"]/dd/ul/li'
    product_style_xpath = './/a[@class="skuLink"]/text()'
    product_price_xpath = './/span[@class="priceVal"]/text()'
    product_availability_xpath = './/p[contains(@class,"availability")]/text()'
    product_name_xpath = '//div[@itemprop="name"]//text()[2]'
    product_brand_xpath = '//div[@itemprop="name"]/span/text()'
    logging.basicConfig(filename='log.txt', level=logging.DEBUG)

    def parse(self, response):
        for href in self.map_links(response, self.main_menu_xpath):
            yield Request(href, callback=self.parse_sub_cats)

    def parse_sub_cats(self, response):
        for href in self.map_links(response, self.sub_menu_xpath):
            yield Request(href, callback=self.parse_product_list)

    def parse_product_list(self, response):
        for href in self.map_links(response, self.product_listing_xpath):
            yield Request(href, callback=self.parse_product)
        if response.xpath('//a[contains(@class,"pageNext")]').extract_first() is not None:
            yield Request(self.get_next_url(response.url), callback=self.parse_product_list)

    def parse_product(self, response):
        for product in response.xpath(self.product_xpath):
            yield self.load_item({
                'url': response.url,
                'style': product.xpath(self.product_style_xpath).extract(),
                'price': product.xpath(self.product_price_xpath).extract(),
                'availability': product.xpath(self.product_availability_xpath).extract(),
                'name': response.xpath(self.product_name_xpath).extract_first(),
                'brand': response.xpath(self.product_brand_xpath).extract_first()
            })

    def load_item(self, item):
        loader = ItemLoader(MusiciansfriendItem())
        for k,v in item.items():
            loader.add_value(k, v)
        return loader.load_item()

    def normalize(self, url):
        url, _ = urldefrag(url)
        return urljoin(self.start_urls[0], url)

    def map_links(self, response, xpath):
        return map(self.normalize, response.xpath(xpath).extract())

    def get_next_url(self, url):
        url = urlparse(url)
        if url.fragment == '':
            return self.start_urls[0] +\
                   url.path +\
                   '#pageName=category-page&Nao=20'
        return self.start_urls[0] +\
               url.path +\
               '#pageName=category-page&Nao=' +\
               str(url.fragment.split('&')[-1].split('=')[-1] + 20)
