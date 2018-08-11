# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlingSystemItem(scrapy.Item):
    # name = scrapy.Field()
    title = scrapy.Field()
    date_time = scrapy.Field()
    news_source = scrapy.Field()
    news_body = scrapy.Field()
    href = scrapy.Field()
    artical_title = scrapy.Field()
    artical_body = scrapy.Field()
    news_md5 = scrapy.Field()
    category = scrapy.Field()
    pass