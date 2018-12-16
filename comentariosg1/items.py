# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Comentariosg1Item(scrapy.Item):
    id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_img_url = scrapy.Field()
    user_oficial = scrapy.Field()
    thumb_up = scrapy.Field()
    thumb_down = scrapy.Field()
    text = scrapy.Field()
    facebook_id = scrapy.Field()
    replies = scrapy.Field()
    original_date = scrapy.Field()
    last_edit_date = scrapy.Field()
    news_url = scrapy.Field()
    news_title = scrapy.Field()
