# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FindChapterItem(scrapy.Item):
    # define the fields for your item here like:
    business_name = scrapy.Field()
    name = scrapy.Field()
    mob = scrapy.Field()
    email = scrapy.Field()
    chapter = scrapy.Field()
   
