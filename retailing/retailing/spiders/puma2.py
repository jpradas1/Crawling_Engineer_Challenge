import scrapy
from scrapy.http.request import Request
import re

class RetailSpider(scrapy.Spider):
    name = "puma2"

    start_urls = []

    base_url = 'https://eu.puma.com'

    custom_settings = {
        # this parameter determine the number of requests in parallel
        # because scrapy is a framework asynchronous
        'CONCURRENT_REQUESTS': 24,

        # restart the process once we ride the spider again
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',

        # encoding
        'FEED_EXPORT_ENCODING': 'utf-8',

        # saving data into json
        # 'FEED_URI': 'puma.json',
        # 'FEED_FORMAT': 'json'

    }

    pid_product_section = ['womens-shoes', 'womens-clothing', 
                           'womens-accessories', 'womens-sport', 
                           'mens-shoes', 'mens-clothing', 
                           'mens-accessories', 'mens-sport', 
                           'kids-boys', 'kids-girls', 
                           'kids-shop-by-product', 'kids-collections', 
                           'kids-shop-by-sports', '', 
                           'collections-lifestyle', 
                           '', '', '', '', '', 
                           'sports-others', 'womens-sale', 
                           'mens-sale', 'kids-sale', 'sale-sports']

    def __init__(self):
        for pid in self.pid_product_section:
            self.start_urls.append(self.request_product_url(pid, -1))

    def request_product_url(self, pid, start):
        request_url = 'https://eu.puma.com/on/demandware.store/Sites-EU-Site/en_DE/Search-UpdateGrid?cgid={}&start={}&sz=36&ajax=true'
        request_url = request_url.format(pid, start)
        return request_url
    
    def product_general_data(self, response):
        pass

    def parse(self, response):

        products = response.xpath('//div[@class="product-tile-info-text"]/a/@href').getall()

        if products:
            for url in products:
                follow_url = self.base_url + url
                yield response.follow(follow_url, callback = self.product_general_data)

        L = lambda x: x.split('cgid=')[1].split('&')[0]
        N = lambda n: int(n.split('start=')[1].split('&')[0]) + 36
        category, page_number = L(response.url), N(response.url)

        