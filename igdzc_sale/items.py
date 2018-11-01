# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class IgdzcSaleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    smallimgurls = scrapy.Field()
    price = scrapy.Field()
    averageprice = scrapy.Field()
    averagepirce=scrapy.Field()
    livingroom = scrapy.Field()
    bedroom = scrapy.Field()
    housesize = scrapy.Field()
    gardenName = scrapy.Field()
    floor = scrapy.Field()
    totalfloor = scrapy.Field()
    direction = scrapy.Field()
    buildyear = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    avator = scrapy.Field()
    sellername = scrapy.Field()
    tel = scrapy.Field()
    lightspot = scrapy.Field()
    mapx = scrapy.Field()
    mapy = scrapy.Field()
    publishtime = scrapy.Field()
    updatetime =scrapy.Field()
    houseid = scrapy.Field()
    areaName = scrapy.Field()

class IgdzcRentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rentPayTypeDesc = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    smallimgurls = scrapy.Field()
    rent = scrapy.Field()
    averagepirce=scrapy.Field()
    livingroom = scrapy.Field()
    bedroom = scrapy.Field()
    housesize = scrapy.Field()
    gardenName = scrapy.Field()
    floor = scrapy.Field()
    totalfloor = scrapy.Field()
    direction = scrapy.Field()
    buildyear = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    avator = scrapy.Field()
    sellername = scrapy.Field()
    tel = scrapy.Field()
    lightspot = scrapy.Field()
    mapx = scrapy.Field()
    mapy = scrapy.Field()
    publishtime = scrapy.Field()
    updatetime =scrapy.Field()
    houseid = scrapy.Field()
    areaName = scrapy.Field()

class IgdzcNewHouseItem(scrapy.Item):
    mapx = scrapy.Field()
    mapy = scrapy.Field()
    addr = scrapy.Field()
    averagePrice = scrapy.Field()
    maxAveragePrice = scrapy.Field()
    buildYear = scrapy.Field()
    plotRatio = scrapy.Field() #容积率
    contactNumber = scrapy.Field()#联系电话
    greeningRate = scrapy.Field()
    lightSpotStr = scrapy.Field()
    projectDesc = scrapy.Field()#项目介绍
    properTypeStr =scrapy.Field()#销售类型
    propertyCompany = scrapy.Field()#物业管理公司
    propertyShow =scrapy.Field()#物业类型
    areaName = scrapy.Field()#地区名字
    developers = scrapy.Field()#开发商
    promoteLanguage = scrapy.Field()#销售口号
    createTime = scrapy.Field()
    registerName = scrapy.Field()
    timeLimit = scrapy.Field()
    buildType = scrapy.Field()
    coversArea = scrapy.Field()#占地面积int
    newHouseId = scrapy.Field()
    houseCost = scrapy.Field()#物业费,str
    carStop = scrapy.Field()
    disparkDateStr = scrapy.Field()#开盘日期
    houseTypeImgUrl =scrapy.Field()#户型图链接
    imgUrlXiaoGuo = scrapy.Field()#效果图片链接
    imgUrlShiJing = scrapy.Field()#实景图片链接
    imgUrlYangBan = scrapy.Field()#样板间图片链接
    houseTypeTit = scrapy.Field()#户型说明
    houseTypeSizeStr = scrapy.Field()#户型面积
    houseTypePriceStr = scrapy.Field()#户型价格
    houseTypeStr = scrapy.Field()#户型其他说明

class IgdzcNewsItem(scrapy.Item):
    content = scrapy.Field()
    newsId = scrapy.Field()
    title = scrapy.Field()
    trimContent = scrapy.Field()
    publishTime = scrapy.Field()
    updateTime = scrapy.Field()
    newsType = scrapy.Field()
    imgUrl = scrapy.Field()
    publishData = scrapy.Field()

class IgdzcGardenItem(scrapy.Item):
    mapx = scrapy.Field()
    mapy = scrapy.Field()
    addr = scrapy.Field()
    averagePrice = scrapy.Field()
    plotRatio = scrapy.Field()
    areaName = scrapy.Field()
    registerName = scrapy.Field()
    gardenId = scrapy.Field()
    propertyTypes = scrapy.Field()

