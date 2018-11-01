# -*- coding: UTF-8 -*-

import scrapy
import urllib2
import os
import re
import codecs
import json
import sys

from scrapy.selector import Selector
from igdzc_sale.items import IgdzcGardenItem 
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from setting_url import defaultUrl
reload(sys)
sys.setdefaultencoding('utf8')

class igdzc_gardenspider(scrapy.Spider):
    name="igdzc_garden"
    allowed_domains=[defaultUrl]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS":{
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Connection':'keep-alive',
            'Host':defaultUrl,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept':'application/json, text/javascript, */*; q=0.01',
            'accept-encoding':'gzip, deflate',
            'accept-language':'zh-CN,zh;q=0.9',
            'origin':'https://'+defaultUrl,
            'Referer': 'http://'+defaultUrl+'/community.html',
            'x-requested-with':'XMLHttpRequest',
            'Cookie': 'JSESSIONID=241F6AC5294D5BC393673C3CBBBCB273; bdshare_firstime=1534229212433; website_cuId=5da753cc-138c-4317-a4d0-4512b5290ce9; website_licenseNo=0121; Hm_lvt_8d2debee9c4cc13193adacef1218a1bf=1540774493,1540784157,1540866265,1540947264; Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf=1540947684'
        },
        "ITEM_PIPELINES":{
            'igdzc_sale.pipelines.IgdzcGardenPipeline': 300
        }
    }

    #设置爬虫属性

    def start_requests(self):
        url = "http://"+defaultUrl+"/houseeb/ebGardenData"
        
        formdata =  {
                     "curPage": "1",
                     "cityId":"329",
                     "pageSize": "10",
                     "bgmapx": "",
                     "edmapx": "",
                     "bgmapy":"",
                     "edmapy": "",
                     "key":"",
                     "sortField":"",
                     "sortType":"",
                     "cuId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}
                        
        yield FormRequest(url,callback=self.parse_igdzc1,formdata=formdata)

    #单发一个请求获取页面数量

    def parse_igdzc1(self,response):
        url = "http://"+defaultUrl+"/houseeb/ebGardenData"
        requests = []
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        count = jsonBody['pageCount']
        for i in range(1,count+1):
            formdata =  {"pageSize": "10",
                        "curPage": str(i),
                        "cityId":"329",
                        "bgmapx": "",
                        "edmapx": "",
                        "bgmapy":"",
                        "edmapy":"",
                        "key":"",
                        "sortField":"",
                        "sortType":"",
                        "cuId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}     
            request = FormRequest(url,callback=self.parse_model,formdata=formdata,dont_filter=True)
            requests.append(request)
        return requests

    #发送请求

    def parse_model(self,response):
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        bodys = jsonBody['items']
        gardenItems=[]
        for dict in bodys:
            gardenItem=IgdzcGardenItem()
            if 'mapx' in dict:
                gardenItem['mapx']=dict['mapx']
            if 'mapy' in dict:
                gardenItem['mapy']=dict['mapy']
            if 'address' in dict:
                gardenItem['addr']=dict['address']
            gardenItem['averagePrice']=0
            if 'averagePrice' in dict:
                gardenItem['averagePrice']=dict['avgPrice']
            gardenItem['plotRatio']=0
            if 'plotRatio' in dict:
                gardenItem['plotRatio']=dict['plotRatio']
            if 'areaName' in dict:
                gardenItem['areaName']=dict['parentAreaName']
            gardenItem['propertyTypes']=dict['propertyTypes']
            gardenItem['registerName']=dict['registerName']
            gardenItem['gardenId']=dict['id']
            gardenItems.append(gardenItem)
        return gardenItems
    #获取返回的数据


