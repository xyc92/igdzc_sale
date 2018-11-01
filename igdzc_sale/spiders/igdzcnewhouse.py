# -*- coding: UTF-8 -*-

import scrapy
import urllib2
import os
import re
import codecs
import json
import sys

from scrapy.selector import Selector
from igdzc_sale.items import IgdzcNewHouseItem 
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from setting_url import defaultUrl
reload(sys)
sys.setdefaultencoding('utf8')

class igdzc_newhousespider(scrapy.Spider):
    name="igdzc_newhouse"
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
            'referer':'http://'+defaultUrl+'/newhouse.html',
            'x-requested-with':'XMLHttpRequest',
            'Cookie': 'JSESSIONID=554DA341AA3042F851E11C182E4AB508; UM_distinctid=16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70; Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1=1530950290,1531185672,1532057705,1532654034; CNZZDATA1272899092=1494324591-1530257238-null%7C1532654832; Hm_lvt_e32b4fcbdc94f23a95000493783dc721=1535936416,1536138372,1536227035,1536282258; website_cuId=5da753cc-138c-4317-a4d0-4512b5290ce9; website_licenseNo=0121; Hm_lvt_8d2debee9c4cc13193adacef1218a1bf=1536114573,1536205438,1536282104,1536543211; Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf=1536543220'
        },
        "ITEM_PIPELINES":{
            'igdzc_sale.pipelines.IgdzcNewHousePipeline': 300
        }
    }

    #设置爬虫属性

    def start_requests(self):
        url = "http://"+defaultUrl+"/houseeb/ebProjectData"
        
        formdata =  {"pageSize": "20",
                     "areaId": "",
                     "curPage":"1",
                     "order": "",
                     "line": "",
                     "key":"",
                     "controlUnitId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}   
        yield FormRequest(url,callback=self.parse_igdzc1,formdata=formdata)

    #单发一个请求获取页面数量

    def parse_igdzc1(self,response):
        url = "http://"+defaultUrl+"/houseeb/ebProjectData"
        requests = []
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        count = jsonBody['pageCount']
        for i in range(1,count+1):
            formdata =  {"pageSize": "20",
                         "areaId": "",
                         "curPage":str(i),
                         "order": "",
                         "line": "",
                         "key":"",
                         "controlUnitId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}   
            request = FormRequest(url,callback=self.parse_model,formdata=formdata,dont_filter=True)
            requests.append(request)
        return requests

    #发送请求

    def parse_model(self,response):
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        bodys = jsonBody['items']
        for dict in bodys:
            HouseItem=IgdzcNewHouseItem()
            if 'mapx' in dict:
                HouseItem['mapx']=dict['mapx']
            if 'mapy' in dict:
                HouseItem['mapy']=dict['mapy']
            if 'addr' in dict:
                HouseItem['addr']=dict['addr']
            if 'averagePrice' in dict:
                HouseItem['averagePrice']=dict['averagePrice']
            if 'maxAveragePirce' in dict:
                HouseItem['maxAveragePirce']=dict['maxAveragePirce']
            if 'buildYear' in dict:
                HouseItem['buildYear']=dict['buildYear']
            if 'plotRatio' in dict:
                HouseItem['plotRatio']=dict['plotRatio']
            if 'contactNumber' in dict:
                HouseItem['contactNumber']=dict['contactNumber']
            if 'greeningRate' in dict:
                HouseItem['greeningRate']=dict['greeningRate']
            HouseItem['lightSpotStr']=''
            if 'lightSpotStr' in dict:
                for i in dict['lightSpotStr']:
                    HouseItem['lightSpotStr']=HouseItem['lightSpotStr']+i
            if 'projectDesc' in dict:
                HouseItem['projectDesc']=dict['projectDesc']
            if 'properTypeStr' in dict:
                HouseItem['properTypeStr']=dict['properTypeStr']
            if 'propertyCompany' in dict:
                HouseItem['propertyCompany']=dict['propertyCompany']
            if 'propertyShow' in dict:
                HouseItem['propertyShow']=dict['propertyShow']
            if 'areaName' in dict:
                HouseItem['areaName']=dict['areaName']
            if 'developers' in dict:
                HouseItem['developers']=dict['developers']
            if 'promoteLanguage' in dict:
                HouseItem['promoteLanguage']=dict['promoteLanguage']
            if 'timeLimit' in dict:
                HouseItem['timeLimit']=dict['timeLimit']
            HouseItem['disparkDateStr']=dict['disparkDateStr']
            HouseItem['newHouseId']=dict['id']
            HouseItem['coversArea']=dict['coversArea']
            HouseItem['buildType']=dict['buildType']
            HouseItem['registerName']=dict['registerName']
            HouseItem['createTime']=dict['createTimeStr']
            HouseItem['houseCost']=dict['houseCost']
            url = dict['staticHtmlUrl']
            url = "http://"+defaultUrl+'/'+url
            yield scrapy.Request(url,meta={'HouseItem':HouseItem},callback=self.parse_detail,cookies={'UM_distinctid':'16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70',
                                                                                                        'Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1':'1530950290,1531185672,1532057705,1532654034',
                                                                                                        'NZZDATA1272899092':'1494324591-1530257238-null%7C1532654832',
                                                                                                        'website_cuId':'5da753cc-138c-4317-a4d0-4512b5290ce9',
                                                                                                        'website_licenseNo':'0121',
                                                                                                        'Hm_lvt_8d2debee9c4cc13193adacef1218a1bf':'1536282104,1536543211,1536626025,1536718374',
                                                                                                        'Hm_lvt_e32b4fcbdc94f23a95000493783dc721':'1536282258,1536550800,1536628395,1536718395',
                                                                                                        'Hm_lpvt_e32b4fcbdc94f23a95000493783dc721':'1536721468',
                                                                                                        'Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf':'1536722103'})
    
    #获取返回的数据

    def parse_detail(self,response):
        HouseItem=response.meta['HouseItem']
        HouseItem['carStop']=response.xpath('//*[@id="LPXQ"]/dl[5]/dd/text()').extract()[0]
        if response.xpath("//dl[@class='house-type']/dt/div/div/@enlarger[.!='']"):
            HouseItem['houseTypeImgUrl']=response.xpath('//dl[@class="house-type"]/dt/div/div/@enlarger').extract()
            HouseItem['houseTypeTit']=response.xpath('//dl[@class="house-type"]/dd/h3/text()').extract()
            HouseItem['houseTypeSizeStr']=response.xpath('//dl[@class="house-type"]/dd/p[1]/text()').extract()
            HouseItem['houseTypePriceStr']=response.xpath('//dl[@class="house-type"]/dd/p[2]/span[2]/text()').extract()
            HouseItem['houseTypeStr']=response.xpath('//dl[@class="house-type"]/dd/ul/li/text()').extract()
        url='http://'+defaultUrl+'/houseeb/newhouse/imagelist?id='+HouseItem['newHouseId']+'&type=RENDERING&cuId=5da753cc-138c-4317-a4d0-4512b5290ce9'
        yield scrapy.Request(url,meta={'HouseItem':HouseItem},callback=self.parse_Img,cookies={'UM_distinctid':'16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70',
                                                                                                        'Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1':'1530950290,1531185672,1532057705,1532654034',
                                                                                                        'NZZDATA1272899092':'1494324591-1530257238-null%7C1532654832',
                                                                                                        'website_cuId':'5da753cc-138c-4317-a4d0-4512b5290ce9',
                                                                                                        'website_licenseNo':'0121',
                                                                                                        'Hm_lvt_8d2debee9c4cc13193adacef1218a1bf':'1536282104,1536543211,1536626025,1536718374',
                                                                                                        'Hm_lvt_e32b4fcbdc94f23a95000493783dc721':'1536282258,1536550800,1536628395,1536718395',
                                                                                                        'Hm_lpvt_e32b4fcbdc94f23a95000493783dc721':'1536721468',
                                                                                                        'Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf':'1536722103'})

    #在新房详情页面获取数据


    def parse_Img(self,response):
        HouseItem=response.meta['HouseItem']
        xiaoGuoStr=response.xpath('//div[@class="search-tabs"]/a[1]/text()').extract()[0].encode('utf-8')
        shiJingStr=response.xpath('//div[@class="search-tabs"]/a[2]/text()').extract()[0].encode('utf-8')
        yangBanStr=response.xpath('//div[@class="search-tabs"]/a[3]/text()').extract()[0].encode('utf-8')
        print xiaoGuoStr+shiJingStr+yangBanStr
        if((xiaoGuoStr.count('0')>0 and len(xiaoGuoStr)==12)==False): #字符串不为'效果图（0）'下面雷同
            HouseItem['imgUrlXiaoGuo']=response.xpath('//*[@id="imgUl1"]/li/img/@src').extract()
        if((shiJingStr.count('0')>0 and len(shiJingStr)==12)==False):
            HouseItem['imgUrlShiJing']=response.xpath('//*[@id="imgUl2"]/li/img/@src').extract()
        if((yangBanStr.count('0')>0 and len(yangBanStr)==12)==False):
            HouseItem['imgUrlYangBan']=response.xpath('//*[@id="imgUl3"]/li/img/@src').extract()
        return HouseItem

    #在图片详情页面获取数据