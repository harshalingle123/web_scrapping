# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyJavascriptItem(scrapy.Item):
    # define the fields for your item here like:
    hone_team = scrapy.Field()
    away_team = scrapy.Field()
    
