# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


class Comentariosg1Item(Item):
    id = Field()
    user_id = Field()
    user_name = Field()
    user_img_url = Field()
    user_oficial = Field()
    thumb_up_id = Field()
    thumb_down_id = Field()
    interaction_id = Field()
    text = Field()
    facebook_id = Field()
    replies = Field()
    original_date = Field()
    last_edit_date = Field()
    news_url = Field()
    news_title = Field()
    aggregator_url = Field()


class Comentariosg1ItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = Comentariosg1Item

    replies_out = Identity()
