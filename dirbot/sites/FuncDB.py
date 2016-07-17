# -*- coding: utf-8 -*-
import adodbapi
import pdb

'''
hostName = "localhost"
dbName = "db1"
tbName = "tbNews"
userName = "csdong"
password = "19860417"
hostName = "176.1.1.154"
dbName = "pub"
tbName = "tbNews"
userName = "ye"
password = "19860417"
'''

def connect(hostName, dbName, userName, password):
    connStr = """Provider=SQLOLEDB.1; User ID=%s; Password=%s;
    Initial Catalog=%s;Data Source= %s"""
    myConnStr = connStr % (userName, password, dbName, hostName)
    myConn = adodbapi.connect(myConnStr)
    return myConn

def query(conn, sql):
    listRows = []
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        listRows.append(row)
        row = cursor.fetchone()
    cursor.close()
    return listRows

def execute(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()

def insertWithListDictOne(conn, listDictOne, tbNameNews, tbNameFulltext=None):
    for dictOne in listDictOne:
        if dictOne.has_key('keywords'):
            strKeyWords = ''
            for keyWord in dictOne['keywords']:
                if strKeyWords == '':
                    strKeyWords = keyWord
                else:
                    strKeyWords = strKeyWords + ',' + keyWord
        else:
            strKeyWords = ''
        
        sql='''
        INSERT INTO dbo.{7} VALUES(
        '{0}', 
        '{1}', 
        '{2}', 
        '{3}',
        '{4}',
        '{5}',
        '{6}'
        )'''.format(
                dictOne['title'].encode('gbk', 'ignore'), 
                dictOne['datetime'].strftime('%Y-%m-%d %H:%M:%S'), 
                dictOne['source'].encode('gbk', 'ignore'), 
                dictOne['link'], 
                strKeyWords.encode('gbk', 'ignore'), 
                dictOne['datetime'].strftime('%Y%m%d'), 
                dictOne['datetime'].strftime('%H:%M:%S'), 
                tbNameNews
                )
        try:
            execute(conn, sql)
        except:
            'Error\n', sql

def insertWithListDictFulltextOne(conn, listDictOne, tbName):
    for dictOne in listDictOne:
        sql='''
        INSERT INTO dbo.{4} VALUES(
        '{0}', 
        '{1}', 
        '{2}', 
        '{3}'
        )'''.format(
                dictOne['title'].encode('gbk', 'ignore'), 
                dictOne['datetime'].strftime('%Y-%m-%d %H:%M:%S'), 
                dictOne['source'].encode('gbk', 'ignore'), 
                dictOne['text'], 
                tbName
                )
        try:
            execute(conn, sql)
        except:
            'Error\n', sql

        print sql

def insertFulltext(conn, listDictOne, tbNameFulltext):
    for dictOne in listDictOne:
        sql='''
        INSERT INTO dbo.{3} VALUES(
        '{0}', 
        '{1}', 
        '{2}' 
        )'''.format(dictOne['title'].encode('gbk', 'ignore'), dictOne['datetime'].strftime('%Y-%m-%d %H:%M:%S'), dictOne['fulltext'].encode('gbk', 'ignore'), tbNameFulltext)
        try:
            execute(conn, sql)
        except:
            print 'Error: insertFulltext\n', sql

