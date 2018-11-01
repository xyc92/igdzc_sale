# -*- coding: UTF-8 -*-

import scrapy
import urllib2
import os
import re
import codecs
import json
import sys
import random
import time

from scrapy.selector import Selector
from igdzc_sale.items import IgdzcNewsItem 
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from setting_url import defaultUrl
reload(sys)
sys.setdefaultencoding('utf8')

class igdzc_newspider(scrapy.Spider):
    name="igdzc_news"
    allowed_domains=[defaultUrl]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS":{
            'Connection':'keep-alive',
            'Conten-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':defaultUrl,
            'accept':'application/json, text/javascript, */*; q=0.01',
            'accept-encoding':'gzip, deflate',
            'accept-language':'zh-CN,zh;q=0.9',
            'origin':'https://'+defaultUrl,
            'referer':'http://'+defaultUrl+'/news.html',
            'x-requested-with':'XMLHttpRequest',
            'Cookie': 'JSESSIONID=554DA341AA3042F851E11C182E4AB508; UM_distinctid=16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70; Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1=1530950290,1531185672,1532057705,1532654034; CNZZDATA1272899092=1494324591-1530257238-null%7C1532654832; Hm_lvt_e32b4fcbdc94f23a95000493783dc721=1535936416,1536138372,1536227035,1536282258; website_cuId=5da753cc-138c-4317-a4d0-4512b5290ce9; website_licenseNo=0121; Hm_lvt_8d2debee9c4cc13193adacef1218a1bf=1536114573,1536205438,1536282104,1536543211; Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf=1536543220'
        },
        "ITEM_PIPELINES":{
            'igdzc_sale.pipelines.IgdzcNewsPipeline': 300
        }
    }

    #设置爬虫属性

    def start_requests(self):
        url = "http://"+defaultUrl+"/houseeb/newsListData"
        
        formdata =  {"pageSize": "10",
                     "curPage":"1",
                     "newsNumber":"ALL",
                     "searchKey":"",
                     "cuId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}   
        yield FormRequest(url,callback=self.parse_igdzc1,formdata=formdata)

    #单发一个请求获取页面数量

    def parse_igdzc1(self,response):
        url = "http://"+defaultUrl+"/houseeb/newsListData"
        requests = []
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        count = jsonBody['pageCount']
        for i in range(1,int(count)+1):
            formdata =  {"pageSize": "10",
                         "curPage":str(i),
                         "newsNumber":"ALL",
                         "searchKey":"",
                         "cuId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}   
            request = FormRequest(url,callback=self.parse_model,formdata=formdata,dont_filter=True)
            requests.append(request)
        return requests

    #发送请求获取ajax

    def parse_model(self,response):
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        bodys = jsonBody['items']
        newsItems = []
        i=0
        for dict in bodys:
            time.sleep(random.random()*1.5)
            newsItem=IgdzcNewsItem()
            newsItem['content']=dict['content']
            newsItem['newsId']=dict['id']
            newsItem['title']=dict['title']
            newsItem['trimContent']=dict['trimContent']
            newsItem['publishTime']=dict['publishDate']['dataValue']
            newsItem['updateTime']=dict['lastUpdateTime']['dataValue']
            newsItem['publishData']=dict['publishDate']['dataValue']
            newsItem['newsType']=dict['informations']['number']
            newsItem['imgUrl']="http://dingjian.img-cn-shenzhen.aliyuncs.com/images/"+dict['imagePath']
            newsItems.append(newsItem)
            i=i+1
            print i
        return newsItems