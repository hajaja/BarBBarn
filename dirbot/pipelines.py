# coding=utf8
import logging
from scrapy.exceptions import DropItem
import pandas as pd
import numpy as np

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['title']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item
######################
# MongoDB
######################
import pymongo
from scrapy.exceptions import DropItem

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "stackoverflow"
MONGODB_COLLECTION = "questions"
class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        db = connection[MONGODB_DB]
        self.collection = db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.log(logging.DEBUG, "blog added to MongoDB database!")
        return item

######################
# MySQL
######################
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

strTB_NewsRaw = 'NewsRaw'

def replaceNanWithNull(sth):
    if sth is '':
        return 'NULL'
    if sth is u'':
        return 'NULL'
    if sth is None:
        return 'NULL'
    if sth == 'None':
        return 'NULL'
    if type(sth) is str or type(sth) is unicode:
        return sth
    return 'NULL' if pd.isnull(sth) else sth


def createTable(strTB):
    con = MySQLdb.connect('localhost', 'csdong', '19860417', 'stock', charset="utf8", use_unicode=True)
    sql = '''
        CREATE TABLE IF NOT EXISTS {0}
        (
          title varchar(100) NOT NULL,
          text text,
          url text,
          source varchar(10) NOT NULL,
          dtCrawled datetime,
          dtCreated datetime,

          CONSTRAINT title_source UNIQUE (title, source)
        )
    '''.format(strTB)
    con.query(sql)
    con.close()
    return

class MySQLPipeline(object):
    def __init__(self):
        try:
            createTable(strTB_NewsRaw)
        except:
            logging.log(logging.ERROR, 'MySQLdb create table error')
            raise Exception

        self.conn = MySQLdb.connect('localhost', 'csdong', '19860417', 'stock', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):    
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        if valid:
            sql = """INSERT IGNORE INTO {0} 
                (title, text, url, source, dtCrawled, dtCreated)
                VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(
                    strTB_NewsRaw,
                    
                    item['title'].encode('utf-8', 'raw_unicode_escape').strip(),
                    item['text'].encode('utf-8', 'raw_unicode_escape'),
                    item['url'],
                    item['source'].encode('utf-8', 'raw_unicode_escape').strip(),
                    replaceNanWithNull(item['dtCrawled']),
                    replaceNanWithNull(item['dtCreated']),
                    )
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        return item
        
        '''
        print 'new item'
        #print item['title']
        #print item['text']
        try:
            sql = """INSERT IGNORE INTO {0} 
                (title, text, url, source, dtCrawled, dtCreated)
                VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(
                    strTB_NewsRaw,

                    item['title'],
                    item['text'],
                    #item['url'],
                    'https://www.baidu.com/',
                    'iFeng',
                    item['dtCrawled'].strftime('%Y-%m-%d %H:%M:%S'),
                    item['dtCreated'],
                    )
        except:
            logging.log(logging.ERROR, item['dtCrawled'])
        print sql
        print 'item end'
        self.cursor.execute(sql)
        self.conn.commit()
        '''


