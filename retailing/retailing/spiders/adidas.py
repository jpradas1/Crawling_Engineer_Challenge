import scrapy

class RetailSpider(scrapy.Spider):
    name = 'adidas'

    start_urls = [
        'https://www.adidas.es/'
    ]

    custom_settings = {
        # this parameter determine the number of requests in parallel
        # because scrapy is a framework asynchronous
        'CONCURRENT_REQUESTS': 24,

        # restart the process once we ride the spider again
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',

        # encoding
        'FEED_EXPORT_ENCODING': 'utf-8',

        # saving data into json
        'FEED_URI': 'adidas.json',
        'FEED_FORMAT': 'json'

    }

    def product_specific(self, response, **kwargs):

        if kwargs:
            title = kwargs['title']

        color_value = response.xpath('//div[@class="color-label___2hXaD"]/text()').get()

        if not color_value:
            color_value =  response.xpath('//div[@class="single-color-label___29kFh"]/text()').get()

        prices = response.xpath('//div[@class="product-description___1TLpA"]//div[@data-auto-id="gl-price-item"]/div[@class]/text()').getall()
        original_price = prices[0]
        current_price = original_price
        
        if len(prices) > 1:
            current_price = prices[1]
            
        images_links = response.xpath('//section[@data-auto-id="image-grid"]//img/@src').getall()
        
        category_path = response.xpath('//ol[@class="breadcrumbs___1S2ES desktop___u0uum"]//span/text()').getall()
        complete_path = ''
        for cp in category_path[1:]:
            complete_path += cp

        complete_path += '/{}'.format(title)
        category_path.append(complete_path)

        data = {
            "title": title,
            "description": '',
            "brand": "ADIDAS",
            "inventory": 'Available',
            "colors": color_value,
            "current_price": current_price,
            "original_price": original_price,
            "sizes": [],
            "url_pictures": images_links,
            "category path": category_path
        }

        yield data

    def product_general(self, response):
        
        title = response.xpath('//h1/span/text()').get()

        color_urls = response.xpath('//div[@class="color-chooser-grid___1ZBx_"]/a/@href').getall()

        if color_urls:
            for url in color_urls:
                follow_url = self.start_urls[0][:-1] + url
                yield response.follow(follow_url, callback=self.product_specific,
                                      cb_kwargs={"title": title})
        
        else:
            yield response.follow(url=response.url, callback=self.product_specific,
                                  cb_kwargs={"title": title})


    def section(self, response):

        products = response.xpath('//div[@class="grid-item"]//a/@href').getall()
        products = list(set(products))

        for url in products:
            follow_url = self.start_urls[0][:-1] + url
            yield response.follow(follow_url, callback=self.product_general)

    def parse(self, response):
        
        categories = response.xpath('//li/a/@href').getall()
        categories = list(set(categories))

        for url in categories:
            follow_url = response.url[:-1] + url
            yield response.follow(follow_url, callback=self.section)