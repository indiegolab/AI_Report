# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCateEachItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    press = scrapy.Field()
    body = scrapy.Field()
    pick = scrapy.Field()
    react = scrapy.Field()
    comment = scrapy.Field()
    recommend = scrapy.Field()
    date = scrapy.Field()
