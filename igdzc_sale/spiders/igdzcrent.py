# -*- coding: utf-8 -*-
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
from igdzc_sale.items import IgdzcRentItem 
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from setting_url import defaultUrl
reload(sys)
sys.setdefaultencoding('utf8')


class igdzc_rentspider(scrapy.Spider):
    name="igdzc_rent"
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
            'referer':'http://'+defaultUrl+'/sale.html',
            'x-requested-with':'XMLHttpRequest',
            'Cookie': 'JSESSIONID=554DA341AA3042F851E11C182E4AB508; UM_distinctid=16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70; Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1=1530950290,1531185672,1532057705,1532654034; CNZZDATA1272899092=1494324591-1530257238-null%7C1532654832; Hm_lvt_e32b4fcbdc94f23a95000493783dc721=1535936416,1536138372,1536227035,1536282258; website_cuId=5da753cc-138c-4317-a4d0-4512b5290ce9; website_licenseNo=0121; Hm_lvt_8d2debee9c4cc13193adacef1218a1bf=1536114573,1536205438,1536282104,1536543211; Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf=1536543220'
        },
        "ITEM_PIPELINES":{
            'igdzc_sale.pipelines.IgdzcRentPipeline': 300
        }        
    }

    def start_requests(self):
        url = "http://"+defaultUrl+"/houseeb/oldhouse/queryListData"
        
        formdata =  {"pageSize": "20",
                     "curPage": "1",
                     "ctId": "329",
                     "feature": "",
                     "key":"",
                     "sortField":"createTime",
                     "sortType":"DESC",
                     "listingType":"RENT",
                     "propertyType":"apartment",
                     "bgmapx":"",
                     "edmapx":"",
                     "bgmapy":"",
                     "edmapy":"",
                     "gardenid":"",
                     "cuId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}   
        yield FormRequest(url,callback=self.parse_igdzc1,formdata=formdata)

    def parse_igdzc1(self,response):
        url = "http://"+defaultUrl+"/houseeb/oldhouse/queryListData"
        requests = []
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        count = jsonBody['pageCount']
        for i in range(1,count+1):
            formdata =  {"pageSize": "20",
                         "curPage": str(i),
                         "ctId": "329",
                         "feature": "",
                         "key":"",
                         "sortField":"createTime",
                         "sortType":"DESC",
                         "listingType":"RENT",
                         "propertyType":"apartment",
                         "bgmapx":"",
                         "edmapx":"",
                         "bgmapy":"",
                         "edmapy":"",
                         "gardenid":"",
                         "cuId":"5da753cc-138c-4317-a4d0-4512b5290ce9"}   
            request = FormRequest(url,callback=self.parse_model,formdata=formdata,dont_filter=True)
            requests.append(request)
        return requests

    def parse_model(self,response):
        directionTable= {
                            "NORTHSOUTH":13,
                            "EASTWEST":14,
                            "SOUTH":15,
                            "NORTH":16,
                            "EAST":17,
                            "WEST":18,
                            "SOUTHEAST":19,
                            "SOUTHWEST":20,
                            "NORTHEAST":21,
                            "NORTHWEST":22
                        }
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        bodys = jsonBody['items']
        for dict in bodys:
            HouseItem=IgdzcRentItem()
            url=""
            HouseItem['areaName']=""
            if 'areaName' in dict:
                HouseItem['areaName']=dict['areaName']
            if 'mapx' in dict:
                HouseItem['mapx']=dict['mapx'] #地图X坐标,str
            if 'mapy' in dict:
                HouseItem['mapy']=dict['mapy'] #地图Y坐标，str
            if 'bedRoom' in dict:
                HouseItem['bedroom']=dict['bedRoom'] #几房，int
            if 'livingRoom' in dict:
                HouseItem['livingroom']=dict['livingRoom'] #几厅,int
            if 'advTitle' in dict:
                HouseItem['title']=dict['advTitle'] #标题,str
            if 'direction' in dict:
                HouseItem['direction']=directionTable[dict['direction']['value']] #朝向,int
            if 'floor' in dict:
                HouseItem['floor']=dict['floor'] #房屋楼层，int
            if 'totalFloor' in dict:
                HouseItem['totalfloor']=dict['totalFloor'] #房屋总楼层,int
            if 'gardenName' in dict:
                HouseItem['gardenName']=dict['gardenName'] #小区名称，str
            if 'description' in dict:
                HouseItem['description']=dict['description'] #销售特色，str
            if 'buildYear' in dict:
                HouseItem['buildyear']=dict['buildYear'] #房源建筑年代，int
            if 'address' in dict:
                HouseItem['address']=dict['address'] #房源所在地址,str
            if 'lightspot' in dict:
                HouseItem['lightspot']=dict['lightspot'] #房源销售介绍，str
            if 'rentPayTypeDesc' in dict:
                HouseItem['rentPayTypeDesc']=dict['rentPayTypeDesc'] #租金支付方式,str
            HouseItem['housesize']=dict['buildArea'] #房源面积,float
            HouseItem['tel']=dict['phone'] #经纪人电话，int
            HouseItem['rent']=dict['rent'] #租金，int
            HouseItem['houseid']=dict['id'] #房源ID，str
            HouseItem['publishtime']=dict['publishTime']['dataValue'] #上传时间，str
            HouseItem['updatetime']=dict['lastUpdateTime']['dataValue'] #更新时间,str
            if 'staticHtmlUrl' in dict:
                url = 'http://'+defaultUrl+'/'+url+dict['staticHtmlUrl']
                ifurl=1
            else:
                ifurl=0
                url = "http://"+defaultUrl+"/houseeb/oldhouse/getInfoById?id="+dict['id']+"&type=esf&cuId="+dict['cuId']
            yield scrapy.Request(url,meta={'HouseItem':HouseItem,'ifurl':ifurl},callback=self.parse_detail,cookies={'UM_distinctid':'16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70',
                                                                                                        'Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1':'1530950290,1531185672,1532057705,1532654034',
                                                                                                        'NZZDATA1272899092':'1494324591-1530257238-null%7C1532654832',
                                                                                                        'website_cuId':'5da753cc-138c-4317-a4d0-4512b5290ce9',
                                                                                                        'website_licenseNo':'0121',
                                                                                                        'Hm_lvt_8d2debee9c4cc13193adacef1218a1bf':'1536282104,1536543211,1536626025,1536718374',
                                                                                                        'Hm_lvt_e32b4fcbdc94f23a95000493783dc721':'1536282258,1536550800,1536628395,1536718395',
                                                                                                        'Hm_lpvt_e32b4fcbdc94f23a95000493783dc721':'1536721468',
                                                                                                        'Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf':'1536722103'},headers={'Referer':'http://'+defaultUrl+''})
    
    def parse_detail(self,response):
        time.sleep(random.random()*1.5)
        HouseItem=response.meta['HouseItem']
        ifurl=response.meta['ifurl']
        HouseItem['smallimgurls']=response.xpath('//*[@id="imgUl"]/li/img/@src').extract()
        HouseItem['company']=response.xpath('//div[@class="img-right"]/dl[4]/dd/text()').extract()[0]
        HouseItem['avator']=response.xpath('//div[@class="broker-brief-details"]/span/a/img/@src').extract()[0]
        if ifurl:
            HouseItem['sellername'] = response.xpath('//div[@class="broker-brief-details"]/p[1]/i[1]/a/text()').extract()[0]
        else:
            HouseItem['sellername'] = response.xpath('//i[@class="ebbroker-name"]/text()').extract()[0]
            i = HouseItem['sellername'].encode('utf-8')
            print i
            i = i[1:len(i)-1]
            print i
            HouseItem['sellername']=i.decode('utf-8')
        return HouseItem