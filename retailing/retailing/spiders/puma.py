import scrapy
from scrapy.http.request import Request
import json, re
from retailing.items import RetailingItem

class RetailSpider(scrapy.Spider):
    name = "puma2"
    start_urls = []

    base_url = 'https://eu.puma.com'
    base_request_url = 'https://eu.puma.com/on/demandware.store/Sites-EU-Site/en_DE/'
    request_product_url = base_request_url + 'Search-UpdateGrid?cgid={}&start={}&sz=36&ajax=true'
    request_product_pid = base_request_url + 'Product-Variations?pid={}&ajax=true'
    request_product_id = 'https://eu.puma.com/de/en/variation?pid={}&dwvar_{}_color={}'

    HEADERS = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        'referer': None
    }

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

    cgid_product_section = ['womens-shoes', 'womens-clothing', 
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
        for cgid in self.cgid_product_section:
            self.start_urls.append(self.request_product_url.format(cgid, 0))

    def crawl_from_api(self, response):
        data = json.loads(response.body)['product']
        images = json.loads(response.body)['pumaImages']

        Items = RetailingItem()

        Items['title'] = data['productName']
        Items['brand'] = 'PUMA'
        Items['description'] = data['shortDescription']
        Items['current_price'] = float(data['price']['sales']['value'])
        Items['original_price'] = Items['current_price']
        
        if data['price']['list']:
            Items['original_price'] = float(data['price']['list']['value'])

        Items['inventory'] = data['analyticsData']['inventory']

        Items['URL_images'] = [x['img']['src'] for x in images['pictures']]
        Items['id'] = data['id']
        Items['color'] = data['variationAttributes'][0]['selectedValue']['displayValue']
        sizes = [x['values'] for x in data['variationAttributes']][-1]
        Items['sizes'] = [x['displayValue'] for x in sizes]
        Items['category_path'] = data['analyticsData']['category'].replace('-', ' > ')

        yield Items

    def get_id_from_api(self, response):
        data = json.loads(response.body)['variations']
        extra_page_urls = [self.base_url + x['pdpLink'] for x in data]
        for link in extra_page_urls:
            ids = re.findall('\d{2,6}', link)[-2:]
            product_id = ids[0]
            color_number = ids[1]

            follow_url = self.request_product_id.format(product_id, product_id, color_number)
            yield Request(url=follow_url, headers=self.HEADERS, callback=self.crawl_from_api)

    def parse(self, response):
        pid_products = response.xpath('//div[@class="grid-tile"]/@data-pid').getall()

        if pid_products:
            for pid in pid_products:
                pid_url = self.request_product_pid.format(pid)
                yield Request(url=pid_url, headers=self.HEADERS, callback=self.get_id_from_api)

        
        #     pid_extract = lambda x: x.split('cgid=')[1].split('&')[0]
        #     start_extract = lambda n: int(n.split('start=')[1].split('&')[0]) + 35

        #     pid, page_number = pid_extract(response.url), start_extract(response.url)
        #     next_page = self.request_product_url.format(pid, page_number)

        #     yield response.follow(next_page, callback = self.parse)