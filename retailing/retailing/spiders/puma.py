import scrapy
import json

class RetailSpider(scrapy.Spider):
    name = 'puma'

    start_urls = [
        'https://eu.puma.com/'
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
        'FEED_URI': 'puma.json',
        'FEED_FORMAT': 'json'

    }

    def product_specific(self, response, **kwargs):
        
        if kwargs:
            title = kwargs['title']
            description =  kwargs['description']
            color = kwargs['color']
            inventory = kwargs['inventory']

        # Specific info: prices, sizes, pictures' urls, categorical path
        current_price = response.xpath('//div[@class="product-tile-price price"]//span[@class="value"]/text()').get()
        original_price = response.xpath('//span[@class="strike-through list"]/span[@class="value"]/text()').get()

        if not original_price:
            original_price = current_price

        sizes = json.loads(response.xpath('//div[@data-component="pdp/ProductSwatches"]/@data-component-options').getall()[1])
        swatches = [x for x in sizes['swatches']]
        sizes = [x['displayValue'] for x in swatches]

        picture_urls = json.loads(response.xpath('//div[@data-component="pdp/ProductImages"]/@data-component-options').get())
        picture_urls = [x['img']['src'] for x in picture_urls['pictures']]

        categorical_path = response.xpath('//ul[@class="breadcrumb"]/li/a/text()').getall()
        categorical_path = [x.strip() for x in categorical_path]

        complete_path = ''
        for cp in categorical_path:
            complete_path += cp + " >> "

        complete_path += title

        categorical_path.append(complete_path)

        data = {
            "title": title,
            "description": description,
            "brand": "PUMA",
            "inventory": inventory,
            "colors": color,
            "current_price": current_price,
            "original_price": original_price,
            "sizes": sizes,
            "url_pictures": picture_urls,
            "category path": categorical_path
        }

        yield data

    def product_general(self, response, **kwargs):

        if kwargs:
            inventory = kwargs['inventory']
        
        # General info as title, description and inventory
        title = response.xpath('//h1[@class="product-name"]/text()').get()
        description = response.xpath('//div[@class="content-slogan-value"]/text()').get()

        # Specific info. First the color which has different images, prices and sizes
        color_urls = json.loads(response.xpath('//div[@data-component="pdp/ProductSwatches"]/@data-component-options').get())
        swatches = [x for x in color_urls['swatches']]
        color_urls = [x['urlProductShow'] for x in swatches]
        color_values = [x['displayValue'] for x in swatches]

        for url, color in zip(color_urls, color_values):
            yield response.follow(url, callback=self.product_specific, 
                                  cb_kwargs={"title": title, "description": description,
                                             "color": color, "inventory": inventory})

    def section(self, response):
        
        products = response.xpath('//div[@class="product-tile-info-text"]/a/@href').getall()

        # first general info, the availability
        inventory = [json.loads(x) for x in response.xpath('//div[@class="grid-tile"]/@data-puma-analytics').getall()]
        inventory = [x['products'][0]['inventory'] for x in inventory]

        for url, inv in zip(products[:2], inventory[:2]):
            follow_url = self.start_urls[0][:-1] + url
            yield response.follow(follow_url, callback = self.product_general,
                                  cb_kwargs={"inventory": inv})

    def parse(self, response):
        
        categories = [response.xpath('//li[@class="p-nav-item js-nav-item"]//div[@class]/a/@href').getall()[0]]
        
        for url in categories:
            follow_url = response.url[:-1] + url
            yield response.follow(follow_url, callback = self.section)
