# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb 
import urllib
import os
import hashlib
import stat
import re
import shutil
import time
from pypinyin import lazy_pinyin, Style
import pypinyin

mysqlUser=""
mysqlPassword=""

areaTable={
                    '大亚湾':1,
                    '惠阳区':2,
                    '惠东县':3,
                    '仲恺区':4,
                    '惠城区':5,
                    '博罗县':6,
                    '龙门县':7,
                    '澳头':8,8:1,
                    '大亚湾澳头':8,
                    '西区':9,9:1,
                    '大亚湾西区':9,
                    '中心区':10,10:1,
                    '霞涌':11,11:1,
                    '淡水':12,12:2,
                    '惠阳经济开发区':13,13:2,
                    '新区中心':14,14:2,
                    '新圩':15,15:2,
                    '永湖':16,16:2,
                    '港口':17,17:3,
                    '黄埠':18,18:3,
                    '平山':19,19:3,
                    '平海':20,20:3,
                    '稔山':21,21:3,
                    '巽寮':22,22:3,
                    '秋长':23,23:2,
                    '响水河':24,24:1
}#地区表

def ifFileCreat(fileRoot):#没有文件就创建
    if(os.path.isfile(fileRoot)==False):
        os.mknod(fileRoot)
        os.chmod(fileRoot,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
        return 1
    return

def ifDirCreat(dirRoot):#没有目录就创建
    if(os.path.isdir(dirRoot)==False):
        os.mkdir(dirRoot)
        os.chmod(dirRoot,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
        return 1
    return

class IgdzcSalePipeline(object):
    def process_item(self,item,spider):
        if(item['areaName'].encode('utf-8') in areaTable):
            areaParentId = areaTable[item['areaName'].encode('utf-8')]
            areaId = areaTable[areaParentId]
            db = MySQLdb.connect("127.0.0.1",mysqlUser,mysqlPassword,"data",unix_socket="/tmp/mysql.sock")
            cursor = db.cursor()
            db.set_character_set('utf8')
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')

            n=cursor.execute("select * from fcw_user where uid=%s",(item['sellername'],))
            avatorUrl=item['avator'].encode('utf-8')
            if(n==0):
                userHash=hashlib.sha1('123456')
                userPw=userHash.hexdigest()
                cursor.execute("INSERT INTO fcw_user(uid,pwd,usertype,sj,uip,nc,email,mot,ifmot,djl,qx,sfzrz,yyzzrz,indexpm,ifqq,zfmm) \
                                VALUES('%s','%s','%d','%s','%s','%s','%s','%s','%d','%d','%s','%d','%d','%d','%d','%s')"%\
                                (item['sellername'],userPw,2,item['publishtime'],'127.0.0.1',item['sellername'],'123@123.com',item['tel']\
                                ,1,0,'2,3,4,5,6,',3,3,0,0,userPw))
                cursor.execute("select * from fcw_user where uid=%s",(item['sellername'],))
                userRow=cursor.fetchone()
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0]))
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f')
                if(avatorUrl.count('hr')):
                    i=ifFileCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                    if(i==1):
                        urllib.urlretrieve(item['avator'],'/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                        os.chmod('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg',stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
            else:
                userRow=cursor.fetchone()
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0]))
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f')
                if(avatorUrl.count('hr')):
                    i=ifFileCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                    if(i==1):
                        urllib.urlretrieve(item['avator'],'/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                        os.chmod('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg',stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
            
            sql ="INSERT INTO fcw_fang(bh,uid,sj,uip,type1,fbty,mot,lxr,wylx,mj,money1,xq,tit,txt,hx1,hx2,lc1,lc2,jznd,fadd,fbsj,zt,ifxj,ifok,cxid,areaid,areaids,djl)\
                    VALUES('%s','%s','%s','%s','%s','%d','%s','%s','%s','%.2f','%.2f','%s','%s','%s','%d','%d','%d','%d','%d','%s','%s','%d','%d','%d','%d','%d','%d','%d')"%\
                    (item['houseid'],item['sellername'],item['updatetime'],'127.0.0.1','出售',2,item['tel'],item['sellername'],'住宅',item['housesize'],\
                    item['price'],item['gardenName'],item['title'],item['lightspot'],item['bedroom'],item['livingroom']\
                    ,item['floor'],item['totalfloor'],item['buildyear'],item['address'],item['publishtime'],0,0,0,item['direction'],areaId,areaParentId,0)

            cursor.execute("select 1 from fcw_fang where bh=%s",(item['houseid'],))
            repetition = cursor.fetchone()
            cursor.execute("select 1 from fcw_tp where bh=%s",(item['houseid'],))
            repetitionImg = cursor.fetchone()
            if repetitionImg: 
                print "重复图片"
            else:
                i=1
                for url in item['smallimgurls']:
                    downloadUrl='/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8')+'/'+str(i)+'.jpg'
                    downloadUrl_smallImg='/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8')+'/'+str(i)+'-1.jpg'
                    if(os.path.isfile(downloadUrl)==False):
                        if(os.path.isdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))==False):
                            os.mkdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))
                        os.mknod(downloadUrl)
                        urllib.urlretrieve(url[:-13],downloadUrl)
                        os.chmod(downloadUrl,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    if(os.path.isfile(downloadUrl_smallImg)==False):
                        if(os.path.isdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))==False):
                            os.mkdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))
                        os.mknod(downloadUrl_smallImg)
                        urllib.urlretrieve(url[:-13]+'@200w_150h_1l',downloadUrl_smallImg)
                        os.chmod(downloadUrl_smallImg,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    downloadUrl='upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8')+'/'+str(i)+'.jpg'
                    cursor.execute("INSERT INTO fcw_tp(bh,tp,type1,sj,uid,xh) VALUES('%s','%s','%s','%s','%s','%d')" %\
                                        (item['houseid'],downloadUrl,'出售',item['updatetime'],'管理员',i))
                    i=i+1

            if repetition: 
                print "重复数据"
            else:
                try:
                        print sql
                        cursor.execute(sql)
                except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            db.commit()
            db.close()
            return item
        else:
            return item

class IgdzcRentPipeline(object):
    def process_item(self,item,spider):
        if(item['areaName'].encode('utf-8') in areaTable):
            areaParentId = areaTable[item['areaName'].encode('utf-8')]
            areaId = areaTable[areaParentId]
            db = MySQLdb.connect("127.0.0.1",mysqlUser,mysqlPassword,"data",unix_socket="/tmp/mysql.sock")
            cursor = db.cursor()
            db.set_character_set('utf8')
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')

            n=cursor.execute("select * from fcw_user where uid=%s",(item['sellername'],))
            avatorUrl=item['avator'].encode('utf-8')
            if(n==0):
                userHash=hashlib.sha1('123456')
                userPw=userHash.hexdigest()
                cursor.execute("INSERT INTO fcw_user(uid,pwd,usertype,sj,uip,nc,email,mot,ifmot,djl,qx,sfzrz,yyzzrz,indexpm,ifqq,zfmm) \
                                VALUES('%s','%s','%d','%s','%s','%s','%s','%s','%d','%d','%s','%d','%d','%d','%d','%s')"%\
                                (item['sellername'],userPw,2,item['publishtime'],'127.0.0.1',item['sellername'],'123@123.com',item['tel']\
                                ,1,0,'2,3,4,5,6,',3,3,0,0,userPw))
                cursor.execute("select * from fcw_user where uid=%s",(item['sellername'],))
                userRow=cursor.fetchone()
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0]))
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f')
                if(avatorUrl.count('hr')):
                    i=ifFileCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                    if(i==1):
                        urllib.urlretrieve(item['avator'],'/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                        os.chmod('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg',stat.S_IRWXO)
            else:
                userRow=cursor.fetchone()
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0]))
                ifDirCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f')
                if(avatorUrl.count('hr')):
                    i=ifFileCreat('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                    if(i==1):
                        urllib.urlretrieve(item['avator'],'/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg')
                        os.chmod('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/user.jpg',stat.S_IRWXO)
            
            sql ="INSERT INTO fcw_fang(bh,uid,sj,uip,type1,fbty,mot,lxr,wylx,mj,money1,xq,tit,txt,hx1,hx2,lc1,lc2,jznd,fadd,fbsj,zt,ifxj,ifok,cxid,djl,jgdw,fkfs,czfs,areaid,areaids)\
                    VALUES('%s','%s','%s','%s','%s','%d','%s','%s','%s','%.2f','%.2f','%s','%s','%s','%d','%d','%d','%d','%d','%s','%s','%d','%d','%d','%d','%d','%s','%s','%d','%d','%d')"%\
                    (item['houseid'],item['sellername'],item['updatetime'],'127.0.0.1','出租',2,item['tel'],item['sellername'],'住宅',item['housesize'],\
                    item['rent'],item['gardenName'],item['title'],item['lightspot'],item['bedroom'],item['livingroom']\
                    ,item['floor'],item['totalfloor'],item['buildyear'],item['address'],item['publishtime'],0,0,0,item['direction'],0,'元/月',item['rentPayTypeDesc'],1,areaId,areaParentId)

            cursor.execute("select 1 from fcw_fang where bh=%s",(item['houseid'],))
            repetition = cursor.fetchone()
            cursor.execute("select 1 from fcw_tp where bh=%s",(item['houseid'],))
            repetitionImg = cursor.fetchone()
            if repetitionImg: 
                print "重复图片"
            else:
                i=1
                for url in item['smallimgurls']:
                    downloadUrl='/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8')+'/'+str(i)+'.jpg'
                    downloadUrl_smallImg='/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8')+'/'+str(i)+'-1.jpg'
                    if(os.path.isfile(downloadUrl)==False):
                        if(os.path.isdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))==False):
                            os.mkdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))
                        os.mknod(downloadUrl)
                        urllib.urlretrieve(url[:-13],downloadUrl)
                        os.chmod(downloadUrl,stat.S_IRWXO)
                    if(os.path.isfile(downloadUrl_smallImg)==False):
                        if(os.path.isdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))==False):
                            os.mkdir('/home/wwwroot/www.5ufc.com/upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8'))
                        os.mknod(downloadUrl_smallImg)
                        urllib.urlretrieve(url[:-13]+'@200w_150h_1l',downloadUrl_smallImg)
                        os.chmod(downloadUrl_smallImg,stat.S_IRWXO)
                    downloadUrl='upload/'+str(userRow[0])+'/f/'+item['houseid'].encode('utf-8')+'/'+str(i)+'.jpg'
                    cursor.execute("INSERT INTO fcw_tp(bh,tp,type1,sj,uid,xh) VALUES('%s','%s','%s','%s','%s','%d')" %\
                                        (item['houseid'],downloadUrl,'出租',item['updatetime'],'管理员',i))
                    i=i+1

            if repetition: 
                print "重复数据！"
            else:
                try:
                        print sql
                        cursor.execute(sql)
                except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            db.commit()
            db.close()                    
            return item
        else:
            return item

class IgdzcNewHousePipeline(object):
    def process_item(self,item,spider):
        directionTable=  {
                            "南北":13,
                            "东西":14,
                            "南":15,
                            "北":16,
                            "东":17,
                            "西":18,
                            "东南":19,
                            "西南":20,
                            "东北":21,
                            "西北":22,
                            "未知":0
                        }
        zhuangXiuTable={
                            "毛坯":5,
                            "豪装":8,
                            "精装":7,
                            "普装":6
        }
        properTypeForPy=''
        properTypeStr=item['properTypeStr'].split(',')
        for i in properTypeStr:
            properTypeForPy=properTypeForPy+'xcf'+i
        properTypeForPy=properTypeForPy+'xcf'
        db = MySQLdb.connect("127.0.0.1",mysqlUser,mysqlPassword,"data",unix_socket="/tmp/mysql.sock")
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        pinyinStrTemp=lazy_pinyin(item['registerName'],style=Style.FIRST_LETTER)
        pinyinStr=''
        for i in pinyinStrTemp:
            pinyinStr=pinyinStr+i

        ifDirCreat('/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8'))

        sql ="INSERT INTO fcw_xq(bh,uid,sj,xq,xqzb,zbdj,py,xqadd,areaid,areaids,money1,wylx,cq,kfs,jzlb,zdmj,rjl,lhl,wygs,wyf,tcw,admin,sltel,sladd,kpsj,lpzt,zt,djl,ifxj,iftj,tjly,xsxh,xqzb1,xqzb2,pyall,txt)\
                VALUES('%s','%s','%s','%s','%s','%d','%s','%s','%d','%d','%.2f','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%s','%s','%d','%d','%d','%d','%d','%s','%d','%s','%s','%s','%s')"%\
                (item['newHouseId'],'管理员',item['createTime'],item['registerName'],item['mapx']+','+item['mapy'],15,'c',item['addr'], \
                areaTable[item['areaName'].encode('utf-8')],0,item['averagePrice'],properTypeForPy,item['timeLimit'],item['developers'],\
                item['buildType'],str(item['coversArea']),str(item['plotRatio']),item['greeningRate'],item['propertyCompany'],\
                item['houseCost'],item['carStop'],2,'400-686-7171',item['addr'],item['disparkDateStr'],0,0,2,0,0,item['lightSpotStr'],9999,item['mapx'],item['mapy'],pinyinStr,item['projectDesc'])

        cursor.execute("select 1 from fcw_xq where bh=%s",(item['newHouseId'],))
        repetition = cursor.fetchone()
        cursor.execute("select 1 from fcw_xqphoto where xqbh=%s",(item['newHouseId'],))
        repetitionImg = cursor.fetchone()
        cursor.execute("select 1 from fcw_huxing where xqbh=%s",(item['newHouseId'],))
        repetitionHouseTypeImg = cursor.fetchone()
        if repetitionHouseTypeImg:
            print "重复户型图"
        else:
            if 'houseTypeImgUrl' in item:
                i=0
                for url in item['houseTypeImgUrl']:
                    downloadUrl='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/huXing'+str(i)+'.jpg'
                    downloadUrl_smallImg='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/huXing'+str(i)+'-1.jpg'
                    
                    if(os.path.isfile(downloadUrl)==False):
                        os.mknod(downloadUrl)
                        urllib.urlretrieve(url,downloadUrl)
                        os.chmod(downloadUrl,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    if(os.path.isfile(downloadUrl_smallImg)==False):
                        os.mknod(downloadUrl_smallImg)
                        urllib.urlretrieve(url+'@200w_150h_1l',downloadUrl_smallImg)
                        os.chmod(downloadUrl_smallImg,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)

                    downloadUrl='huXing'+str(i)

                    print item['houseTypeTit'][i].encode('utf-8')
                    houseTypeTitTemp='0室0厅'
                    if(re.search('\S室\S厅',item['houseTypeTit'][i].encode('utf-8'))):
                        houseTypeTitTemp=re.search('\S室\S厅',item['houseTypeTit'][i].encode('utf-8')).group()
                    houseTypeSizeStrTemp=item['houseTypeSizeStr'][i].encode('utf-8').split('：')[1]
                    houseTypeSize=float(houseTypeSizeStrTemp.split('平')[0])
                    houseTypeDirecionStr=item['houseTypeStr'][i].encode('utf-8').split(' ')[2]
                    houseTypeZhuangXiu=0
                    if(item['houseTypeStr'][i].encode('utf-8').split(' ')[3]!=''):
                        houseTypeZhuangXiu=zhuangXiuTable[item['houseTypeStr'][i].encode('utf-8').split(' ')[3]]
                    houseTypePriceTemp=item['houseTypePriceStr'][i].encode('utf-8')
                    houseTypePrice=0.0
                    if(houseTypePriceTemp.count('元')>0):
                        houseTypePrice=int(houseTypePriceTemp.split('元')[0])*houseTypeSize/10000
                    elif(houseTypePriceTemp!='万'):
                        houseTypePrice=float(houseTypePriceTemp.split('万')[0])

                    cursor.execute("INSERT INTO fcw_huxing(uid,tit,mj,hx1,hx2,hx3,hx4,hx5,sj,xqbh,bh,cx,zxqkid,fwlcid,money1,djl,areaid,areaids,zt,iftj) \
                                    VALUES('%s','%s','%.2f','%d','%d','%d','%d','%d','%s','%s','%s','%d','%d','%d','%.2f','%d','%d','%d','%d','%d')" %\
                                    ('管理员',item['houseTypeTit'][i],houseTypeSize,int(houseTypeTitTemp[0]),\
                                    int(houseTypeTitTemp[4]),0,0,0,item['createTime'],item['newHouseId'],downloadUrl,directionTable[houseTypeDirecionStr],\
                                    houseTypeZhuangXiu,0,houseTypePrice,0,areaTable[item['areaName'].encode('utf-8')],0,0,0))
                    i=i+1
        
        #对抓取的户型图进行处理
        
        if repetitionImg: 
            print "重复图片"
        else:
            if 'imgUrlXiaoGuo' in item:
                i=1
                for url in item['imgUrlXiaoGuo']:
                    downloadUrl='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/xiaoGuo'+str(i)+'.jpg'
                    downloadUrl_smallImg='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/xiaoGuo'+str(i)+'-1.jpg'
                    if(os.path.isfile(downloadUrl)==False):
                        os.mknod(downloadUrl)
                        urllib.urlretrieve(url,downloadUrl)
                        os.chmod(downloadUrl,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    if(os.path.isfile(downloadUrl_smallImg)==False):
                        os.mknod(downloadUrl_smallImg)
                        urllib.urlretrieve(url+'@200w_150h_1l',downloadUrl_smallImg)
                        os.chmod(downloadUrl_smallImg,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    downloadUrl='xiaoGuo'+str(i)+'.jpg'
                    cursor.execute("INSERT INTO fcw_xqphoto(uid,xqbh,sj,tit,djl,bh,zt,tyid,areaid,areaids,iffm) VALUES('%s','%s','%s','%s','%d','%s','%d','%d','%d','%d','%d')" %\
                                    ('管理员',item['newHouseId'],item['createTime'],item['registerName']+'效果图',0,'xiaoGuo'+str(i),0,2,areaTable[item['areaName'].encode('utf-8')],0,0))
                    i=i+1
            if 'imgUrlShiJing' in item: 
                i=1       
                for url in item['imgUrlShiJing']:
                    downloadUrl='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/shiJing'+str(i)+'.jpg'
                    downloadUrl_smallImg='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/shiJing'+str(i)+'-1.jpg'
                    if(os.path.isfile(downloadUrl)==False):
                        os.mknod(downloadUrl)
                        urllib.urlretrieve(url,downloadUrl)
                        os.chmod(downloadUrl,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    if(os.path.isfile(downloadUrl_smallImg)==False):
                        os.mknod(downloadUrl_smallImg)
                        urllib.urlretrieve(url+'@200w_150h_1l',downloadUrl_smallImg)
                        os.chmod(downloadUrl_smallImg,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    downloadUrl='shiJing'+str(i)+'.jpg'
                    cursor.execute("INSERT INTO fcw_xqphoto(uid,xqbh,sj,tit,djl,bh,zt,tyid,areaid,areaids,iffm) VALUES('%s','%s','%s','%s','%d','%s','%d','%d','%d','%d','%d')" %\
                                    ('管理员',item['newHouseId'],item['createTime'],item['registerName']+'实景图',0,'shiJing'+str(i),0,1,areaTable[item['areaName'].encode('utf-8')],0,0))
                    i=i+1

            if 'imgUrlYangBan' in item:
                i=1
                for url in item['imgUrlYangBan']:
                    downloadUrl='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/yangBan'+str(i)+'.jpg'
                    downloadUrl_smallImg='/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/yangBan'+str(i)+'-1.jpg'
                    if(os.path.isfile(downloadUrl)==False):
                        os.mknod(downloadUrl)
                        urllib.urlretrieve(url,downloadUrl)
                        os.chmod(downloadUrl,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    if(os.path.isfile(downloadUrl_smallImg)==False):
                        os.mknod(downloadUrl_smallImg)
                        urllib.urlretrieve(url+'@200w_150h_1l',downloadUrl_smallImg)
                        os.chmod(downloadUrl_smallImg,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
                    downloadUrl='yangBan'+str(i)+'.jpg'
                    cursor.execute("INSERT INTO fcw_xqphoto(uid,xqbh,sj,tit,djl,bh,zt,tyid,areaid,areaids,iffm) VALUES('%s','%s','%s','%s','%d','%s','%d','%d','%d','%d','%d')" %\
                                    ('管理员',item['newHouseId'],item['createTime'],item['registerName']+'样板房',0,'yangBan'+str(i),0,5,areaTable[item['areaName'].encode('utf-8')],0,0))
                    i=i+1
            if(os.path.isfile('/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/home.jpg')==False):
                ifFileCreat('/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/home.jpg')
                if(os.path.isfile('/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/xiaoGuo1-1.jpg')):
                    shutil.copy('/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/xiaoGuo1-1.jpg','/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/home.jpg')
                elif(os.path.isfile('/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/shiJing1-1.jpg')):
                    shutil.copy('/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/shiJing1-1.jpg','/home/wwwroot/www.5ufc.com/upload/3/f/'+item['newHouseId'].encode('utf-8')+'/home.jpg')
                    
        #对抓取的图片进行处理
                
        if repetition: 
            print "重复数据！"
        else:
            try:
                    print sql
                    cursor.execute(sql)
            except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        db.commit()
        db.close()                    
        return item

class IgdzcNewsPipeline(object):
    def process_item(self,item,spider):
        newsTypeTable={
                        "goufangbaike":25,
                        "redianshiping":26,
                        "dayawanfangxun":27,
                        "zhifanggonglue":28,
                        "shikanershoufang":29,
                        "xinfangdaogou":30,
                        "loushidiaokong":31
        }
        if (item['newsType'].encode('utf-8') in newsTypeTable)==False:
            return item
        db = MySQLdb.connect("127.0.0.1",mysqlUser,mysqlPassword,"data",unix_socket="/tmp/mysql.sock")
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        i=1
        print item['newsType'].encode('utf-8')
        if(item['imgUrl']==""):
            i=0
        
        sql ="INSERT INTO fcw_news(type1id,type2id,tit,djl,sj,lastsj,uip,bh,iftj,indextop,ifjc,titys,wdes,zt,iftp,txt)\
                VALUES('%d','%d','%s','%d','%s','%s','%s','%s','%d','%d','%d','%s','%s','%d','%d','%s')"%\
                (newsTypeTable[item['newsType'].encode('utf-8')],0,item['title'],0,item['publishTime'],item['updateTime'],'127.0.0.1',\
                item['newsId'],1,0,1,'#333',item['trimContent'],0,i,item['content'])


        cursor.execute("select 1 from fcw_tp where bh=%s",(item['newsId'],))
        repetitionImg = cursor.fetchone()
        cursor.execute("select 1 from fcw_news where bh=%s",(item['newsId'],))
        repetition = cursor.fetchone()
        if i==0:
            print "没图片！"
        elif repetitionImg:
            print "重复图片！"
        else:
            downloadUrl='/home/wwwroot/www.5ufc.com/upload/news/'+item['publishData']+'/'+item['newsId']+'/newsImg1.jpg'
            downloadUrl_smallImg='/home/wwwroot/www.5ufc.com/upload/news/'+item['publishData']+'/'+item['newsId']+'/newsImg1-1.jpg'
            ifDirCreat('/home/wwwroot/www.5ufc.com/upload/news/'+item['publishData'])
            ifDirCreat('/home/wwwroot/www.5ufc.com/upload/news/'+item['publishData']+'/'+item['newsId'])
            if(os.path.isfile(downloadUrl)==False):
                os.mknod(downloadUrl)
                urllib.urlretrieve(item['imgUrl'],downloadUrl)
                os.chmod(downloadUrl,stat.S_IRWXO)
            if(os.path.isfile(downloadUrl_smallImg)==False):
                os.mknod(downloadUrl_smallImg)
                urllib.urlretrieve(item['imgUrl']+'@200w_150h_1l',downloadUrl_smallImg)
                os.chmod(downloadUrl_smallImg,stat.S_IRWXO)
            downloadUrl='upload/news/'+item['publishData']+'/'+item['newsId']+'/newsImg1.jpg'
            cursor.execute("INSERT INTO fcw_tp(bh,tp,type1,sj,xh) VALUES('%s','%s','%s','%s','%d')" %\
                                    (item['newsId'],downloadUrl,'资讯',item['updateTime'],1))
        if repetition: 
            print "重复数据！"
        else:
            try:
                    print sql
                    cursor.execute(sql)
            except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        db.commit()
        db.close()                    
        return item

class IgdzcGardenPipeline(object):
    def process_item(self,item,spider):
        if(item['areaName'].encode('utf-8') in areaTable):
            areaParentId = areaTable[item['areaName'].encode('utf-8')]
            db = MySQLdb.connect("127.0.0.1",mysqlUser,mysqlPassword,"data",unix_socket="/tmp/mysql.sock")
            cursor = db.cursor()
            db.set_character_set('utf8')
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')

            pinyinStrTemp=lazy_pinyin(item['registerName'],style=Style.FIRST_LETTER)
            pinyinStr=''
            for i in pinyinStrTemp:
                pinyinStr=pinyinStr+i

            propertyTypeTemp=item['propertyTypes'].encode('utf-8')
            propertyType='xcf'
            if propertyTypeTemp.count('APARTMENT'):
                propertyType=propertyType+'住宅xcf'
            if propertyTypeTemp.count('SHOP'):
                propertyType=propertyType+'商铺xcf'


            sql ="INSERT INTO fcw_xq(bh,uid,sj,xq,xqzb,py,xqadd,areaid,money1,wylx,cq,kfs,rjl,admin,zt,djl,ifxj,xqzb1,xqzb2,pyall)\
                    VALUES('%s','%s','%s','%s','%s','%s','%s','%d','%.2f','%s','%s','%s','%s','%d','%d','%d','%d','%s','%s','%s')"%\
                    (item['gardenId'],'管理员',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),item['registerName'],\
                    item['mapx']+','+item['mapy'],'c',item['addr'],areaParentId,item['averagePrice'],propertyType,'暂无数据','暂无数据',\
                    str(item['plotRatio']),1,0,0,0,item['mapx'],item['mapy'],pinyinStr)

            cursor.execute("select 1 from fcw_xq where bh=%s",(item['gardenId'],))
            repetition = cursor.fetchone()

            if repetition: 
                print "重复数据！"
            else:
                try:
                        print sql
                        cursor.execute(sql)
                except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            db.commit()
            db.close()                    
            return item
        else:
            return item
