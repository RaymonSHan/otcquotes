# -*- coding:gbk -*-
#
# Althought I do not input any Chinese in my project, I still insert this progma before any codes.
# Recommen GBK instead of Unicode or UTF-8 in any case.
#
# Wrapping Column 132.
import scrapy
import otcconfigure

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
            xpathlist = string.xpath('string(' + number[2:] +')').extract()
            if xpathlist:
                xpathresult = xpathlist[0].strip()
                if xpathresult:
                    return int(xpathresult)
        else:
            print 'error format', number
    else:
        print 'error type', type(number)
    return -1

HTTP_OK    = 200
TotalCrawl = True
StringList = ['stockname', 'stocknewprice', 'stocktotalamount']
FormatList = [ string + '_format' for string in StringList]
DStringList = ['d_stocknumber', 'd_stockfullname', 'd_stockstart', 'd_stockweb']
DFormatList = [ string + '_format' for string in DStringList]

def GetListofString(stockinfo, onestock, oneotc, stringlist, formatlist):
    for order in xrange(0, len(stringlist)):
        oneformatlist = formatlist[order]
        onestringlist = stringlist[order]
        if oneformatlist in oneotc.keys() and oneotc[oneformatlist]:
#            stockinfo[onestringlist] = onestock.xpath('string('+oneotc[oneformatlist]+')').extract()[0].strip()
            infolist = onestock.xpath(oneotc[oneformatlist]+'/text()').extract()
            if infolist:
                stockinfo[onestringlist] = infolist[0].strip()
            else:
                stockinfo[onestringlist] = ''
        else:
            stockinfo[onestringlist] = ''
    return stockinfo

class AllQuotes(scrapy.Spider):
    name = 'AllQuotes'
# set allowed_domains empty to allow all request
    allowed_domains = []
    HTTPERROR_ALLOW_ALL = True

    def start_requests(self):
        for oneotc in otcconfigure.OTC_SITES:
            # in lambda is val para, in call() is ref para, VERY IMPORTANT !!!
            request = scrapy.Request(oneotc['homepage'], self.parse_list)
            request.meta['oneotc'] = oneotc
            yield request

    def parse_list(self, response):
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return

        oneotc = response.meta['oneotc']
# should do more for multi page list
        pagestart = GetFormatNumber(oneotc['startpage'])
# range(1,2) only run once
        pageend = GetFormatNumber(oneotc['endpage'], response) + 1
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
            print 'is there'
            request = scrapy.Request(onepageurl, self.parse_page)
            request.meta['oneotc'] = oneotc
            yield request

    def parse_page(self, response):
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return
        oneotc = response.meta['oneotc']
        if not oneotc['stock_format']:
            return

        for onestock in response.xpath(oneotc['stock_format'])[:3]:   ####### should remove after test
            stockformatlist = onestock.xpath(oneotc['stockid_format']).extract()
            if stockformatlist:
                stockformat = stockformatlist[0]
            else:
                continue
            stocklengthstart = GetFormatNumber(oneotc['stock_length_start'], stockformat)
            stocklengthend = GetFormatNumber(oneotc['stock_length_end'], stockformat, stocklengthstart)
            if stocklengthstart == -1 or stocklengthend == -1:
                continue
            onestockid = stockformat[stocklengthstart : stocklengthend]

            stockinfo = {}
            GetListofString(stockinfo, onestock, oneotc, StringList, FormatList)
#            onestockname = onestock.xpath(oneotc['stocktotalamount_format']+'/text()').extract()[0]
#            print 'onestockname', onestockname, type(onestockname)
            print stockinfo


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


            print 'onestockurl' , onestockurl
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

#        onestocknumber = onestock.xpath(oneotc['d_stockweb_format']+'/text()').extract()[0]
#        print 'onestocknumber', onestocknumber, type(onestocknumber)
        GetListofString(stockinfo, onestock, oneotc, DStringList, DFormatList)
        print stockinfo

    @staticmethod 
    def parse_tianjin(response):
        print 'in tianjin', response.url
            
    @staticmethod
    def statictest():
        print 'asdf'


class TestQuotes(scrapy.Spider):
    name = 'Quotes'
    start_urls = ['http://www.tjsoc.com/web/homepage.aspx?name=schq']
    def parse(self, response):
        for onestock in response.xpath('//table[@id="ContentPlaceHolder1_GridView1"]//tr[@onclick]'):
#            print onestock
            stockid = onestock.xpath('./@onclick').extract()[0]
            print stockid

if __name__ == '__main__':
   name = 'asdf'
   room = 234
   website = 'http'
   aaa = "MY name is:%s\nMy room is:%d\nMy website is:%s"%(name,room,website)
   print aaa
   test = AllQuotes()
   AllQuotes.statictest()
   print AllQuotes.name
   print test.name

