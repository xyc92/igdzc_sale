# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class IgdzcSaleUrlItem(scrapy.Item):
    url = scrapy.Field()


class IgdzcSaleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    special = scrapy.Field()
    smallimgurls = scrapy.Field()
    price = scrapy.Field()
    bathroom = scrapy.Field()
    bedroom = scrapy.Field()
    housesize = scrapy.Field()
    decoration = scrapy.Field()
    floor = scrapy.Field()
    totalfloor = scrapy.Field()
    direction = scrapy.Field()
    buildyear = scrapy.Field()
    community = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    avator = scrapy.Field()
    sellername = scrapy.Field()
    tel = scrapy.Field()
    introduction = scrapy.Field()
    selleridea = scrapy.Field()
    housenearby = scrapy.Field()
    houseservice = scrapy.Field()
    mapx = scrapy.Field()
    mapy = scrapy.Field()
    publishtime = scrapy.Field()
    updatetime =scrapy.Field()

class IgdzcRentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    special = scrapy.Field()
    smallimgurls = scrapy.Field()
    price = scrapy.Field()
    room = scrapy.Field()
    housesize = scrapy.Field()
    decoration = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    buildyear = scrapy.Field()
    community = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    avator = scrapy.Field()
    sellername = scrapy.Field()
    tel = scrapy.Field()
    introduction = scrapy.Field()
    selleridea = scrapy.Field()
    housenearby = scrapy.Field()
    houseservice = scrapy.Field()
    mapx = scrapy.Field()
    mapy = scrapy.Field()
    publishtime = scrapy.Field()



