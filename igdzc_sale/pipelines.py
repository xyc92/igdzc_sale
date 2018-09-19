# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb 

class IgdzcSaleUrlPipeline(object):
    def process_item(self,item,spider):
        db = MySQLdb.connect("localhost","root","","spider",unix_socket="/tmp/mysql.sock")
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        sql ="INSERT INTO db_url(url) VALUES('%s')"%(item['url'])

        cursor.execute("select 1 from db_url where url =%s",(item['url'],))
        repetition = cursor.fetchone()
        if repetition: 
            print "123"
        else:
            try:
                    print sql
                    cursor.execute(sql)
                    db.commit()
            except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            db.close()
        return item
