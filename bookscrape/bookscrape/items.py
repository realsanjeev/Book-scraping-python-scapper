# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    url = scrapy.Field()
    upc = scrapy.Field()
    name = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field()
    genre = scrapy.Field()
    availability = scrapy.Field()
    no_of_reviews = scrapy.Field()
    stars = scrapy.Field()
    description = scrapy.Field()
