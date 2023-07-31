# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    quotes = scrapy.Field()

class AuthorScrapeItem(scrapy.Item):
    name = scrapy.Field()
    birthday = scrapy.Field()
    genre = scrapy.Field()
    influences = scrapy.Field()
    birthplace = scrapy.Field()
    description = scrapy.Field()
