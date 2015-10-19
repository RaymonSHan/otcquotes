# -*- coding:gbk -*-
#
# Althought I do not input any Chinese in my project, I still insert this progma before any codes.
# Recommen GBK instead of Unicode or UTF-8 in any case.
#
# Wrapping Column 132.
import scrapy
import json
import otcconfigure

# for signals in scarpy, such as dispatcher.connect(self.initialize, signals.engine_started) 
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

def GetFormatNumber(number, string = '', start = 0):
    if isinstance(number, int):
        return number
    elif isinstance(number, str):
        functionkey = number[:1]
        if functionkey == 'S':
            ret = string.find(number[2:])
            if ret != -1: 
                return ret + len(number) - 2 # remove the start 'S:'
        elif functionkey == 'E':
            ret = string[start:].find(number[2:])
            if ret != -1: 
                return ret + start
        elif functionkey == 'X':
            xpathlist = string.xpath(number[2:]).extract()
            print 'xpathlist', xpathlist
            if xpathlist:
                xpathresult = xpathlist[0].strip()
                if xpathresult:
                    return xpathresult
        else:
            print 'error format', number
    else:
        print 'error type', type(number)
    return -1

def GetSubString(key, oneotc, string):
    startkey = key + '_s'
    endkey = key + '_e'
    startnum = -1
    endnum = -1
    print 'in getsubstring key', key
    print oneotc
    print  string
    if startkey in oneotc.keys() and oneotc[startkey]:
        startnum = GetFormatNumber(oneotc[startkey], string)
    if startnum != -1 and endkey in oneotc.keys() and oneotc[endkey]:
        endnum = GetFormatNumber(oneotc[endkey], string, startnum)
    print 'after key', startnum, endnum, type(startnum), type(endnum), string[startnum: endnum]
    if startnum == -1:
        startnum = 0
    if endnum == -1:
        endnum = len(string)
    return int(string[startnum: endnum])

def GetFormatSubString(key, oneotc, response):
    firstreturn = GetFormatNumber(oneotc[key], response)
    print 'firstreturn', firstreturn, type(firstreturn)
    if isinstance(firstreturn, int):
        return firstreturn
    elif isinstance(firstreturn, str) or isinstance(firstreturn, unicode):
        return GetSubString(key, oneotc, firstreturn)
    else:
        return -1

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

    try:
        xpathresult = response.xpath(realxpathkey).extract()[0].strip()
    except:
        return ''
    if xpathkeynumber >= 2:
        resultstart = GetNumberByFind(xpathkey[1], xpathresult) + len(xpathkey[1])
        print 'in >= 2', xpathkey[1], xpathresult, resultstart
    else:
        resultstart = 0
    if xpathkeynumber >= 3:
        resultend = GetNumberByFind(xpathkey[2], xpathresult[resultstart:]) + resultstart
        print 'in >= 3', xpathkey[2], xpathresult, resultend
    else:
        resultend = len(xpathresult)
    return xpathresult[resultstart : resultend]
    

HTTP_OK    = 200
TotalCrawl = True
StringList = ['stockname', 'stocknewprice', 'stocktotalamount', 'stocktodaymount']
FormatList = [ string + '_format' for string in StringList]
DStringList = ['d_stocknumber', 'd_stockfullname', 'd_stockstart', 'd_stockweb']
DFormatList = [ string + '_format' for string in DStringList]

def GetListofString(stockinfo, onestock, oneotc, stringlist, formatlist):
    for order in xrange(0, len(stringlist)):
        oneformatlist = formatlist[order]
        onestringlist = stringlist[order]
        if oneformatlist in oneotc.keys() and oneotc[oneformatlist]:
#            stockinfo[onestringlist] = onestock.xpath('string('+oneotc[oneformatlist]+')').extract()[0].strip()
            infolist = onestock.xpath(oneotc[oneformatlist]).extract()
            if infolist:
                stockinfo[onestringlist] = infolist[0].strip().encode('utf-8')
            else:
                stockinfo[onestringlist] = ''
        else:
            stockinfo[onestringlist] = ''
    return stockinfo

    
def DisplayStockInfo(totalstock):
    for onestock in totalstock:
        for oneattr in onestock.keys():
            print oneattr + ' : ' + onestock[oneattr] + ',\t',
        print ''
    print 'total : ', len(totalstock)

class AllQuotes(scrapy.Spider):
    name = 'AllQuotes'
# set allowed_domains empty to allow all request
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
        for oneotc in otcconfigure.OTC_SITES:
            # in lambda is val para, in call() is ref para, VERY IMPORTANT !!!
            request = scrapy.Request(oneotc['homepage'], self.parse_start)
            request.meta['oneotc'] = oneotc
            yield request

    def parse_start(self, response):
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return

        oneotc = response.meta['oneotc']
        pagestart = int(GetStringByXpath(oneotc['startpage'], response))
#        pagestart = GetFormatNumber(oneotc['startpage'])
# range(1,2) only run once
        pageend = int(GetStringByXpath(oneotc['endpage'], response)) + 1
        print 'pagestart end', pagestart, pageend
#        pageend = GetFormatNumber(oneotc['endpage'], response) + 1
        if pagestart == -1 or pageend == -1:
            return
        pageparalist = []

        quotesurl = oneotc['quotes_url']
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
        if not oneotc['stock_format']:
            return

        for onestock in response.xpath(oneotc['stock_format'])[:3]:   
#        for onestock in response.xpath(oneotc['stock_format']):
            print 'onestock', onestock
            onestockid = GetStringByXpath(oneotc['stockid_format'], onestock)
            print 'onestockid', onestockid
#            stockformatlist = onestock.xpath(oneotc['stockid_format']).extract()

#            if stockformatlist:
#                stockformat = stockformatlist[0]
#            else:
#                continue
#            stocklengthstart = GetFormatNumber(oneotc['stock_length_start'], stockformat)
#            stocklengthend = GetFormatNumber(oneotc['stock_length_end'], stockformat, stocklengthstart)
#            if stocklengthstart == -1 or stocklengthend == -1:
#                continue
#            onestockid = stockformat[stocklengthstart : stocklengthend]

            stockinfo = {}
            GetListofString(stockinfo, onestock, oneotc, StringList, FormatList)

            if not TotalCrawl:
                # output stockinfo with key otc.shortname + onestockid
# stock detail info should not crawl everytime
                return
            stockparalist = []
            if not 'stock_url' in oneotc.keys() or not oneotc['stock_url']:
                return
            stockdetail = oneotc['stock_url']
            if stockdetail.find('{stockid}') != -1:
                stockparalist.append('stockid=onestockid')
            stockurl = "onestockurl = stockdetail.format(" + ",".join(stockparalist) + ")"
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
        if not 'd_stock_format' in oneotc.keys() or not oneotc['d_stock_format']:
            return

        stockinfo = response.meta['info']
        onestocklist = response.xpath(oneotc['d_stock_format'])
        if onestocklist:
            onestock = onestocklist[0]
        else:
            return

        GetListofString(stockinfo, onestock, oneotc, DStringList, DFormatList)
        stockinfo['stockinfo_url'] = response.url
        stockinfo['d_stocknumber'] = ''.join([stockinfo['d_stocknumber'], '.' + oneotc['shortname']])
        self.TotalStock.append(stockinfo)




