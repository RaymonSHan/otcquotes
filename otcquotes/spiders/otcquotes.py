# -*- coding:gbk -*-
#
# Althought I do not input any Chinese in my project, I still insert this progma before any codes.
# Recommen GBK instead of Unicode or UTF-8 in any case.
#
# Wrapping Column 132.
import scrapy
import json
from otcconfigure import *

# for signals in scarpy, such as dispatcher.connect(self.initialize, signals.engine_started) 
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher



import MySQLdb
import datetime

import time

exampleinfo = {
'StockIdInListPage' : '52', 'StockTodayAmount' : 110, 'StockNewPrice' : 1.65, 'StockId' : '52.ah', 'StockName' : '开元软件',
}

'''	
StockIdInListPage : 54,	StockTodayAmount : 0,	StockNewPrice : 0.98,	StockId : 54.ah,	StockName : 黄山一建,	
StockIdInListPage : 55,	StockTodayAmount : 0,	StockNewPrice : 4.0,	StockId : 55.ah,	StockName : 朝晖股份,	
StockIdInListPage : 103,	StockTodayAmount : 0,	StockNewPrice : 1.06,	StockId : 103.ah,	StockName : 新方舟,	
'''

def GeneratorSQLxxx(stockinfo, columndictall):
    stockinfo[UPDATETIME] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    columndict = columndictall[1]
    columnvalue = columndict.values()
    stockvalue = [stockinfo.get(key, 0) for key in columndict.keys()]
    questionvalue = ['?' for key in xrange(0, len(columndict))]
    
    sql_insert = 'insert into '+columndictall[0]+'('+','.join(columnvalue)+') values ('+','.join(questionvalue)+')'
    print columnvalue
    print stockvalue
    print questionvalue
    print sql_insert
        


if __name__ == '__main__':
    stockinfo = {}
    GeneratorSQL(exampleinfo, GLOBAL_INFO[DATABASEQUOTATION])

def notused():
    try:

        sql_content = "insert into table(key1,key2,key3) values (?,?,?)"
        cur.execute(sql_content,(value1,value2,value3))

        conn=MySQLdb.connect(host='192.168.206.139',user='root',passwd='',db='mysql',port=3306)
        cur=conn.cursor()

        value=[1,'hi rollen']
        cur.execute('insert into test values(%s,%s)',value)
        "insert into table(key1,key2,key3) values (%s,%s,%s)"%(value1,value2,value3)

        count=cur.execute('select * from user')
        result=cur.fetchone()
        print result, type(result)
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


HTTP_OK                         = 200

DATATYPEDICT = {
  'int'                         : [
    STOCKTODAYAMOUNT, STOCKTOTALAMOUNT,
  ],
  'float'                       : [
    STOCKNEWPRICE,
  ],
}

def GetStockDetail(stockinfo, infodict, response):              # here stockinfo is ref para
    for oneinfokey in infodict.keys():
        if oneinfokey:
            oneinforesult = GetStringByXpath(infodict[oneinfokey], response)
            if oneinfokey in DATATYPEDICT['int']:
                try:
                    stockinfo[oneinfokey] = int(oneinforesult)
                except:
                    stockinfo[oneinfokey] = int(0)
            elif oneinfokey in DATATYPEDICT['float']:
                try:
                    stockinfo[oneinfokey] = float(oneinforesult)
                except:
                    stockinfo[oneinfokey] = float(0)
            else:
                stockinfo[oneinfokey] = oneinforesult
        else:
            oneinforesult = ''
            stockinfo[oneinfokey] = oneinforesult

def GetNumberByFind(key, result):
    if isinstance(key, int):
        return key
    elif isinstance(key, str) or isinstance(key, unicode):
        place = result.find(key)
        if place != -1:
            return place
        else:
            raise

def GetStringByXpath(xpathkey, response):
    if isinstance(xpathkey, list):
        xpathkeynumber = len(xpathkey)
        if xpathkeynumber >= 1:
            realxpathkey = xpathkey[0]
        else:
            return ''
    elif isinstance(xpathkey, int):
        return str(xpathkey)
    elif isinstance(xpathkey, str) or isinstance(xpath, unicode):
        xpathkeynumber = 0
        realxpathkey = xpathkey
    else:
        return ''
    if not realxpathkey:
        return ''

    try:
        xpathresult = response.xpath(realxpathkey).extract()[0].strip().encode('utf-8')
    except:
        return ''
    if xpathkeynumber > POS_START:
        resultstart = GetNumberByFind(xpathkey[1], xpathresult) + len(xpathkey[1])
    else:
        resultstart = 0
    if xpathkeynumber > POS_END:
        resultend = GetNumberByFind(xpathkey[2], xpathresult[resultstart:]) + resultstart
    else:
        resultend = len(xpathresult)
    return xpathresult[resultstart : resultend]
    
def DisplayStockInfo(totalstock):
    for onestock in totalstock:
        for oneattr in onestock.keys():
            print oneattr + ' : ' + str(onestock[oneattr]) + ',\t',
        print ''
    print 'total : ', len(totalstock)

def JoinDictionary(localdict, globaldict):
    for onekey in globaldict:
        if not onekey in localdict:
            localdict[onekey] = globaldict[onekey]
        elif isinstance(localdict[onekey], dict) and isinstance(globaldict[onekey], dict):
            JoinDictionary(localdict[onekey], globaldict[onekey])

def FormatStockInfo(oneotc, stockinfo, response, displayformat):
    if not displayformat:
        return stockinfo

    newinfo = stockinfo
    for onedetail in displayformat.keys():
        displayparaplist = []
        oneformat = displayformat[onedetail]

        if oneformat.find('{STOCKNUMBER}') != -1:
            displayparaplist.append('STOCKNUMBER=stockinfo[STOCKNUMBER]')
        if oneformat.find('{ABBRNAME}') != -1:
            displayparaplist.append('ABBRNAME=oneotc[ABBRNAME]')
        if oneformat.find('{STOCKURL}') != -1:
            displayparaplist.append('STOCKURL=response.url')
        if oneformat.find('{ONESTOCKID}') != -1:
            displayparaplist.append('ONESTOCKID=stockinfo[ONESTOCKID]')

        displayexec = 'newinfo[onedetail] = oneformat.format(' + ','.join(displayparaplist) + ')'
        exec(displayexec)
    return newinfo

class AllQuotes(scrapy.Spider):
    name = 'otcquotes'
    allowed_domains = []
    HTTPERROR_ALLOW_ALL = True

    def __init__(self):
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def initialize(self):
        self.TotalStock = []
 
    def finalize(self):
        DisplayStockInfo(self.TotalStock)
        with open('stockjson', 'wb') as f:
            f.write(json.dumps(self.TotalStock, ensure_ascii=False))
 
    def start_requests(self):
        for oneotc in OTC_SITES:
            JoinDictionary(oneotc, GLOBAL_INFO)
            request = scrapy.Request(oneotc[HOMEPAGE_URL], self.parse_start)
            request.meta['oneotc'] = oneotc
            yield request

    def parse_start(self, response):
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return

        oneotc = response.meta['oneotc']
        pagenumber = GetStringByXpath(oneotc[PAGESTART], response)
        if pagenumber:
            pagestart = int(pagenumber)
        else:
            return
        pagenumber = GetStringByXpath(oneotc[PAGEEND], response)
        if pagenumber:
# range(1,2) only run once
            pageend = int(pagenumber) + 1
        else:
            return

        pageparalist = []
        if not ONEPAGE_URL in oneotc.keys() or not oneotc[ONEPAGE_URL]:
            return
        quotesurl = oneotc[ONEPAGE_URL]
        if quotesurl.find('{pagenum}') != -1:
            pageparalist.append('pagenum=onepage')
        pageurl = "onepageurl = quotesurl.format(" + ",".join(pageparalist) + ")"

        for onepage in range(pagestart, pageend):
# onepageurl now is the url, should be send as request
            exec(pageurl)
            request = scrapy.Request(onepageurl, self.parse_list)
            request.meta['oneotc'] = oneotc
            yield request

    def parse_list(self, response):
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return
        oneotc = response.meta['oneotc']
        if not ONESTOCK_FORMAT in oneotc.keys() or not oneotc[ONESTOCK_FORMAT]:
            return

        for onestockinlist in response.xpath(oneotc[ONESTOCK_FORMAT]):   
            onestockid = GetStringByXpath(oneotc[ONESTOCKID], onestockinlist)
            if not onestockid:
                continue

            stockinfo = {}
            stockinfo[ONESTOCKID] = onestockid
            GetStockDetail(stockinfo, oneotc[LISTPAGEDETAIL], onestockinlist)

            if not TOTAL_CRAWL:
# stock detail info should not crawl everytime
                formatedstockinfo = FormatStockInfo(oneotc, stockinfo, response, oneotc[DISPLAYINFOPRICE])
                self.TotalStock.append(formatedstockinfo)
                continue

            stockparalist = []
            if not DETAILSTOCK_URL in oneotc.keys() or not oneotc[DETAILSTOCK_URL]:
                continue
            stockdetail = oneotc[DETAILSTOCK_URL]
            if stockdetail.find('{stockid}') != -1:
                stockparalist.append('stockid=onestockid')
            stockurl = 'onestockurl = stockdetail.format(' + ','.join(stockparalist) + ')'
            exec(stockurl)

            request = scrapy.Request(onestockurl, self.parse_stock)
            request.meta['oneotc'] = oneotc
            request.meta['info'] = stockinfo
            yield request

    def parse_stock(self, response):
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return
        oneotc = response.meta['oneotc']
        stockinfo = response.meta['info']

        if not DETAILSTOCK_FORMAT in oneotc.keys() or not oneotc[DETAILSTOCK_FORMAT]:
            onestockdetail = response
        else:
            onestockdetail = response.xpath(oneotc[DETAILSTOCK_FORMAT])
        GetStockDetail(stockinfo, oneotc[STOCKPAGEDETAIL], onestockdetail)

        if stockinfo[STOCKNUMBER]:
            formatedstockinfo = FormatStockInfo(oneotc, stockinfo, response, oneotc[DISPLAYINFODETAIL])
            self.TotalStock.append(formatedstockinfo)


'''
CREATE TABLE `quotes`.`stock_quotation` (
  `line_number` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(32) NOT NULL,
  `stock_price` FLOAT NULL DEFAULT 0,
  `stock_totalamount` INT NULL DEFAULT 0,
  `stock_todayamount` INT NULL DEFAULT 0,
  `update_time` DATETIME NOT NULL,
  PRIMARY KEY (`line_number`));
'''
