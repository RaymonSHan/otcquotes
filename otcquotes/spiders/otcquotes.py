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
        if functionkey == 'E':
            ret = string[start:].find(number[2:])
            if ret != -1: 
                return ret + start
    else:
        print 'error type', type(number)
    return -1

HTTP_OK    = 200
TotalCrawl = True
StringList = ['stockname', 'stocknewprice', 'stocktotalamount']
FormatList = [ string + '_format' for string in StringList]

def GetListofString(onestock, oneotc, stringlist, formatlist):
    stockdetail = {}
    for order in xrange(0, len(stringlist)):
        oneformatlist = formatlist[order]
        onestringlist = stringlist[order]
        if oneformatlist in oneotc.keys() and oneotc[oneformatlist]:
            stockdetail[onestringlist] = onestock.xpath('string('+oneotc[oneformatlist]+')').extract()[0]
        else:
            stockdetail[onestringlist] = ''
    return stockdetail

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
        oneotc = response.meta['oneotc']
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return

# should do more for multi page list
        pagestart = GetFormatNumber(oneotc['startpage'])
# range(1,2) only run once
        pageend = GetFormatNumber(oneotc['endpage']) + 1
        pageparalist = []

        quotesurl = oneotc['quotes_url']
        if quotesurl.find('{pagenum}') != -1:
            pageparalist.append('pagenum=onepage')
        pageurl = "onepageurl = quotesurl.format(" + ",".join(pageparalist) + ")"

        for onepage in range(pagestart, pageend):
# onepageurl now is the url, should be send as request
            exec(pageurl)
            request = scrapy.Request(onepageurl, self.parse_page)
            request.meta['oneotc'] = oneotc
            yield request

    def parse_page(self, response):
        oneotc = response.meta['oneotc']
        status = response.status
        if status != HTTP_OK:
            print 'Error in get %s, httpstatus : %d' %(response.url, status)
            return
        if not oneotc['stock_format']:
            return
        for onestock in response.xpath(oneotc['stock_format'])[:3]:
            stockformat = onestock.xpath(oneotc['stockid_format']).extract()[0]
            stocklengthstart = GetFormatNumber(oneotc['stock_length_start'], stockformat)
            stocklengthend = GetFormatNumber(oneotc['stock_length_end'], stockformat, stocklengthstart)
            onestockid = stockformat[stocklengthstart : stocklengthend]

            stockinfo = GetListofString(onestock, oneotc, StringList, FormatList)
#            onestockname = onestock.xpath('string('+oneotc['stockname_format']+')').extract()[0]
#            onestocknewprice = onestock.xpath('string('+oneotc['stocknewprice_format']+')').extract()[0]
#            onestocktotalamount = onestock.xpath('string('+oneotc['stocktotalamount_format']+')').extract()[0]
#            print onestockname, onestocknewprice, onestocktotalamount

            if not TotalCrawl:
# stock detail info should not crawl everytime
                return
            stockparalist = []
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
        print response.meta['info']



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

