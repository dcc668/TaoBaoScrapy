# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class TaobaoscrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #商品信息
    img = Field()
    actPrice = Field()
    mPrice = Field()
    tagPrice = Field()
    title = Field()
    url = Field()
    #店家信息

    pass
