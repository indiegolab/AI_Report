# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlerItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    press = scrapy.Field()
    body = scrapy.Field()
    pick = scrapy.Field()
    react = scrapy.Field()
    comment = scrapy.Field()
    recommend = scrapy.Field()