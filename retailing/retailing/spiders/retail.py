import scrapy

class RetailSpider(scrapy.Spider):
    name = 'retails'

    start_urls = [
        'https://www.adidas.es/'
    ]

    def parse(self, response):
        
        print('\n\n')
        # genre = reponse.xpath('//ul[@data-auto-id="main-menu"]/li/text()').getall()
        categories = response.xpath('//li/a/@href').getall()
        # categoires = []
        print(categories)
        print('\n\n')