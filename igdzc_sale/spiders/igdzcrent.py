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
reload(sys)
sys.setdefaultencoding('utf8')


class igdzc_rentspider(scrapy.Spider):
    name="igdzc_rent"
    allowed_domains=['igdzc.com']
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS":{
            'Connection':'keep-alive',
            'Conten-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.igdzc.com',
            'accept':'application/json, text/javascript, */*; q=0.01',
            'accept-encoding':'gzip, deflate',
            'accept-language':'zh-CN,zh;q=0.9',
            'origin':'https://www.igdzc.com',
            'referer':'http://www.igdzc.com/sale.html',
            'x-requested-with':'XMLHttpRequest',
            'Cookie': 'JSESSIONID=554DA341AA3042F851E11C182E4AB508; UM_distinctid=16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70; Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1=1530950290,1531185672,1532057705,1532654034; CNZZDATA1272899092=1494324591-1530257238-null%7C1532654832; Hm_lvt_e32b4fcbdc94f23a95000493783dc721=1535936416,1536138372,1536227035,1536282258; website_cuId=5da753cc-138c-4317-a4d0-4512b5290ce9; website_licenseNo=0121; Hm_lvt_8d2debee9c4cc13193adacef1218a1bf=1536114573,1536205438,1536282104,1536543211; Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf=1536543220'
        }
     }

    def start_requests(self):
        url = "http://www.igdzc.com/houseeb/oldhouse/queryListData"
        
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
        url = "http://www.igdzc.com/houseeb/oldhouse/queryListData"
        requests = []
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        count = jsonBody['count']
        for i in range(1,int(count)/20+2):
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
        jsonBody = json.loads(response.body.decode('utf-8').encode('utf-8'))
        bodys = jsonBody['items']
        for dict in bodys:
            HouseItem=IgdzcRentItem()
            url=""
            if 'mapx' in dict:
                HouseItem['mapx']=dict['mapx']
            if 'mapy' in dict:
                HouseItem['mapy']=dict['mapy']
            if 'bathRoom' in dict:
                HouseItem['bathroom']=dict['bathRoom']
            if 'bedRoom' in dict:
                HouseItem['bedroom']=dict['bedRoom']
            if 'advTitle' in dict:
                HouseItem['title']=dict['advTitle']
            if 'averagePrice' in dict:
                HouseItem['price']=dict['averagePrice']
            if 'direction' in dict:
                HouseItem['direction']=dict['direction']['value']
            if 'floor' in dict:
                HouseItem['floor']=dict['floor']
            if 'totalFloor' in dict:
                HouseItem['totalfloor']=dict['totalFloor']
            if 'gardenName' in dict:
                HouseItem['decoration']=dict['gardenName']
            HouseItem['publishtime']=dict['publishTime']['dataValue']
            HouseItem['updatetime']=dict['lastUpdateTime']['dataValue']
            if 'staticHtmlUrl' in dict:
                url = 'http://www.igdzc.com/'+url+dict['staticHtmlUrl']
            else:
                url = "http://www.igdzc.com/houseeb/oldhouse/getInfoById?id="+dict['id']+"&type=esf&cuId="+dict['cuId']
            if 'address' in dict:
                HouseItem['address']=dict['address']
            if 'buildYear' in dict:
                HouseItem['buildyear']=dict['buildYear']
            HouseItem['publishtime']=dict['publishTime']['dataValue']
            yield scrapy.Request(url,meta={'HouseItem':HouseItem},callback=self.parse_detail,cookies={'UM_distinctid':'16439e2e9285a1-026736dca9a45-601a147a-fa000-16439e2e92a70',
                                                                                                        'Hm_lvt_957975d81c9f19b4eb2f2d63f78cf9a1':'1530950290,1531185672,1532057705,1532654034',
                                                                                                        'NZZDATA1272899092':'1494324591-1530257238-null%7C1532654832',
                                                                                                        'website_cuId':'5da753cc-138c-4317-a4d0-4512b5290ce9',
                                                                                                        'website_licenseNo':'0121',
                                                                                                        'Hm_lvt_8d2debee9c4cc13193adacef1218a1bf':'1536282104,1536543211,1536626025,1536718374',
                                                                                                        'Hm_lvt_e32b4fcbdc94f23a95000493783dc721':'1536282258,1536550800,1536628395,1536718395',
                                                                                                        'Hm_lpvt_e32b4fcbdc94f23a95000493783dc721':'1536721468',
                                                                                                        'Hm_lpvt_8d2debee9c4cc13193adacef1218a1bf':'1536722103'},headers={'Referer':'http://www.igdzc.com'})
    
    def parse_detail(self,response):
        time.sleep(random.random()*1.5)
        HouseItem=response.meta['HouseItem']
        HouseItem['special']=response.xpath('//*[@id="description"]/@value').extract()
        HouseItem['smallimgurls']=response.xpath('//*[@id="imgUl"]/li/img/@src').extract()
        HouseItem['price']=response.xpath('//div[@class="brief-01"]/span/em/text()').extract()
        HouseItem['housesize']=response.xpath('//ul[@class="brief-02"]/li[2]/p[2]/em/text()').extract()
        HouseItem['community']=response.xpath('//div[@class="img-right"]/dl[3]/dd/a/text()').extract()
        HouseItem['company']=response.xpath('//div[@class="img-right"]/dl[4]/dd/text()').extract()
        HouseItem['avator']=response.xpath('//div[@class="broker-brief-details"]/span/a/img/@src').extract()
        HouseItem['sellername']=response.xpath('//div[@class="broker-brief-details"]/p[1]/i[1]/a/text()').extract()
        HouseItem['tel']=response.xpath('//div[@class="broker-brief-details"]/p[2]/text()').extract()
        HouseItem['introduction']=response.xpath('//*[@id="FYMS"]/div[1]/text()').extract()
        HouseItem['selleridea']=response.xpath('//*[@id="FYMS"]/div[2]/text()').extract()
        HouseItem['housenearby']=response.xpath('//*[@id="FYMS"]/div[3]/text()').extract()
        HouseItem['houseservice']=response.xpath('//*[@id="FYMS"]/div[4]/text()').extract()
        return HouseItem