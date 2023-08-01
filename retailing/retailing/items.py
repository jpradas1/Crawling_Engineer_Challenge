# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RetailingItem(scrapy.Item):
    title = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    current_price = scrapy.Field()
    original_price = scrapy.Field()
    inventory = scrapy.Field()
    URL_images = scrapy.Field()
    id = scrapy.Field()
    color = scrapy.Field()
    sizes = scrapy.Field()
    category_path = scrapy.Field()