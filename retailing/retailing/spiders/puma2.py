import scrapy
from scrapy.http.request import Request
import re

class RetailSpider(scrapy.Spider):
    name = "puma2"

    HEADERS = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        'referer': None
    }

    start_urls = ["https://eu.puma.com/"]

    request_product = 'https://eu.puma.com/on/demandware.store/Sites-EU-Site/en_DE/Search-UpdateGrid?cgid={}&start={}&sz={}&ajax=true'

    def product_section(self, response):
        pass

    def parse(self, response):
        categories = response.xpath('//li[@class="p-nav-item js-nav-item"]//div[@class]/a/@href').getall()


        
        for url in categories:
            follow_url = response.url[:-1] + url
            yield response.follow(follow_url, callback = self.product_section)