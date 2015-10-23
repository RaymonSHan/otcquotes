# -*- coding:utf-8 -*-
#
# Wrapping Column 132.

FULLNAME                        = 'ExchangeName'
ABBRNAME                        = 'ExchangeAbbreviateName'
HOMEPAGE_URL                    = 'ExchangeListPage'
PAGESTART                       = 'StartPageNumberInList'
PAGEEND                         = 'EndPageNumberInList'
ONEPAGE_URL                     = 'StockListPage'
ONESTOCK_FORMAT                 = 'StockFormatInListPage'
ONESTOCKID                      = 'StockIdInListPage'           # stockid is used in htmlpage, may not same as stocknumber

DETAILSTOCK_URL                 = 'StockDetailPage'
DETAILSTOCK_FORMAT              = 'StockFormatInStockPage'

LISTPAGEDETAIL                  = 'AllItemInListPage'
STOCKPAGEDETAIL                 = 'AllItemInStockPage'

DISPLAYINFOPRICE                = 'DisplayInfoPrice'
DISPLAYINFODETAIL               = 'DisplayInfoDetail'

STOCKID                         = 'StockId'
STOCKNAME                       = 'StockName'
STOCKFULLNAME                   = 'StockFullName'
STOCKNUMBER                     = 'StockNumber'
STOCKNEWPRICE                   = 'StockNewPrice'

STOCKTODAYAMOUNT                = 'StockTodayAmount'
STOCKTOTALAMOUNT                = 'StockTotalAmount'

STOCKOPENDATE                   = 'StockOpenDate'
STOCKHOMEPAGE                   = 'StockHomePage'

STOCKINFOURL                    = 'StockInfoURL'
UPDATETIME                      = 'CrawlTime'

DATABASEQUOTATION               = 'DatabaseQuotation'
DATABASEDETAIL                  = 'DatabaseDetail'

POS_XPATH                       = 0
POS_START                       = 1
POS_END                         = 2

POS_TABLE                       = 0
POS_COLUMN                      = 1

TOTAL_CRAWL                     = True

DATATYPEDICT = {
  'int'                         : [
    STOCKTODAYAMOUNT, STOCKTOTALAMOUNT,
  ],
  'float'                       : [
    STOCKNEWPRICE,
  ],
}

GLOBAL_INFO                     = {
    DISPLAYINFOPRICE            : {
      STOCKID                   : '{ONESTOCKID}.{ABBRNAME}',
    },
    DISPLAYINFODETAIL           : {
      STOCKID                   : '{ONESTOCKID}.{ABBRNAME}',
      STOCKNUMBER               : '{STOCKNUMBER}.{ABBRNAME}', 
      STOCKINFOURL              : '{STOCKURL}',
    },

    DATABASEQUOTATION           : ['quotes.stock_quotation',
    {
      STOCKID                   : 'stock_id',
      STOCKNEWPRICE             : 'stock_price',
      STOCKTOTALAMOUNT          : 'stock_totalamount',
      STOCKTODAYAMOUNT          : 'stock_todayamount',
      UPDATETIME                : 'update_time',
    } ],
    DATABASEDETAIL              : ['quotes.stock_detail',
    {
      STOCKID                   : 'stock_id',
      STOCKNUMBER               : 'stock_number',
      STOCKNAME                 : 'stock_name',
      STOCKFULLNAME             : 'stock_fullname',
      STOCKHOMEPAGE             : 'stock_website',
      STOCKOPENDATE             : 'stock_opendate',
      STOCKINFOURL              : 'stock_infourl',
      UPDATETIME                : 'update_time',
    } ],
}

OTC_SITES                       = [
  { FULLNAME                    : 'AnHui Equity Exchange',
    HOMEPAGE_URL                : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005',
    ABBRNAME                    : 'ah',
    PAGESTART                   : 1,
    PAGEEND                     : 1,
#    PAGEEND                     : '//div[@class="page"]/font/text()',
    ONEPAGE_URL                 : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005&pageno={pagenum}&pagesize=10',
    ONESTOCK_FORMAT             : '//table[@class="tab03"]/tr',
    ONESTOCKID                  : ['./td[1]/span/a/@href', 'id='],
    LISTPAGEDETAIL              : {
      STOCKNAME                 : './td[2]/a/text()',
      STOCKNEWPRICE             : './td[3]/span/text()',
      STOCKTODAYAMOUNT          : './td[4]/text()',
    },
    DETAILSTOCK_URL             : 'http://www.ahsgq.com/aee/bm/bminfo.jsp?id={stockid}',
    DETAILSTOCK_FORMAT          : '//table[@class="tab05"]',
    STOCKPAGEDETAIL             : {
      STOCKNUMBER               : './tr[3]/td[1]/text()',
      STOCKFULLNAME             : './tr[1]/td[1]/text()',
      STOCKOPENDATE             : './tr[7]/td[1]/text()',
      STOCKHOMEPAGE             : './tr[11]/td[1]/text()',
    },
  },
]

OTC_SITES_OK                    = [
  { FULLNAME                    : 'TianJin Equity Exchange',
    HOMEPAGE_URL                : 'http://www.tjsoc.com/',
    ABBRNAME                    : 'tj',
    PAGESTART                   : 1,
    PAGEEND                     : 1,
    ONEPAGE_URL                 : 'http://www.tjsoc.com/web/homepage.aspx?name=schq',
    ONESTOCK_FORMAT             : '//table[@id="ContentPlaceHolder1_GridView1"]//tr[@onclick]',
    ONESTOCKID                  : ['./@onclick', 'code=', '\''],
# in html it is <table style="..."><tr><td>, but it change to <table><tr><td><font>
    LISTPAGEDETAIL              : {
      STOCKNAME                 : './td[1]/font/text()',
      STOCKNEWPRICE             : './td[2]/font/text()',
      STOCKTOTALAMOUNT          : './td[3]/font/text()',
    },
    DETAILSTOCK_URL             : 'http://www.tjsoc.com/web/seksun.aspx?code={stockid}',
    DETAILSTOCK_FORMAT          : '//div[@class="mainbox"]//table',
    STOCKPAGEDETAIL             : {
      STOCKNUMBER               : './tr[2]/td[2]/span/text()',
      STOCKFULLNAME             : './tr[3]/td[2]/span/text()',
      STOCKOPENDATE             : './tr[4]/td[2]/span/text()',
      STOCKHOMEPAGE             : './tr[7]/td[2]/a/text()',
    },
    DISPLAYINFODETAIL           : {
      STOCKNUMBER               : '{STOCKNUMBER}.{ABBRNAME}', 
      STOCKINFOURL              : '{STOCKURL}',
    },
  },
  { FULLNAME                    : 'ShangHai Equity Exchange',
    HOMEPAGE_URL                : 'http://www.china-see.com/stockInfo.do',
    ABBRNAME                    : 'sh',
    PAGESTART                   : 1,
    PAGEEND                     : '//div[@id="dropdown3"]/ul/li[last()]/a/text()',
    ONEPAGE_URL                 : 'http://www.china-see.com/stockInfo.do?pageNo={pagenum}',
    ONESTOCK_FORMAT             : '//div[@class="wrap1Rsub"]//table/tr',
    ONESTOCKID                  : './td[1]/text()',
    LISTPAGEDETAIL              : {
      STOCKNAME                 : './td[2]/text()',
      STOCKNEWPRICE             : './td[3]/text()',
      STOCKTOTALAMOUNT          : './td[13]/div/text()',
    },
    DETAILSTOCK_URL             : 'http://www.china-see.com/f10.do?tabIndex=1&stockCode={stockid}',
    DETAILSTOCK_FORMAT          : '//div[@class="tabcon"]/table',
    STOCKPAGEDETAIL             : {
      STOCKNUMBER               : './tr[4]/td[1]/text()',
      STOCKFULLNAME             : './tr[1]/td[1]/text()',
      STOCKOPENDATE             : './tr[9]/td[1]/text()',
      STOCKHOMEPAGE             : './tr[13]/td[1]/text()',
    },
  },
  { FULLNAME                    : 'AnHui Equity Exchange',
    HOMEPAGE_URL                : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005',
    ABBRNAME                    : 'ah',
    PAGESTART                   : 1,
    PAGEEND                     : '//div[@class="page"]/font/text()',
    ONEPAGE_URL                 : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005&pageno={pagenum}&pagesize=10',
    ONESTOCK_FORMAT             : '//table[@class="tab03"]/tr',
    ONESTOCKID                  : ['./td[1]/span/a/@href', 'id='],
    LISTPAGEDETAIL              : {
      STOCKNAME                 : './td[2]/a/text()',
      STOCKNEWPRICE             : './td[3]/span/text()',
      STOCKTODAYAMOUNT          : './td[4]/text()',
    },
    DETAILSTOCK_URL             : 'http://www.ahsgq.com/aee/bm/bminfo.jsp?id={stockid}',
    DETAILSTOCK_FORMAT          : '//table[@class="tab05"]',
    STOCKPAGEDETAIL             : {
      STOCKNUMBER               : './tr[3]/td[1]/text()',
      STOCKFULLNAME             : './tr[1]/td[1]/text()',
      STOCKOPENDATE             : './tr[7]/td[1]/text()',
      STOCKHOMEPAGE             : './tr[11]/td[1]/text()',
    },
  },
  { FULLNAME                    : 'Qilu Equity Exchange',
    HOMEPAGE_URL                : 'http://www.zbotc.com/hangqing-guapai-list.php',
    ABBRNAME                    : 'zb',
    PAGESTART                   : 1,
    PAGEEND                     : ['//td[@width="153"]/div/text()', '/', ')'],
    ONEPAGE_URL                 : 'http://www.zbotc.com/hangqing-guapai-list.php?page={pagenum}',
    ONESTOCK_FORMAT             : '//table[@id="Table41"]//table/tr[@height="32" and position()>1]',
    ONESTOCKID                  : './td[2]/a/text()',
    LISTPAGEDETAIL              : {
      STOCKNUMBER               : './td[2]/a/text()',
      STOCKNAME                 : './td[3]/a/text()',
      STOCKNEWPRICE             : './td[4]/text()',
      STOCKTODAYAMOUNT          : './td[5]/text()',
      STOCKTOTALAMOUNT          : './td[7]/div/text()',
    },
    DETAILSTOCK_URL             : 'http://www.qlotc.cn/guquan-guapai-{stockid}.html',
    DETAILSTOCK_FORMAT          : '//div[@class="head"]/div/dl/dd',
    STOCKPAGEDETAIL             : {
      STOCKFULLNAME             : './span[1]/h1/text()',
      STOCKHOMEPAGE             : './span[3]/text()',
    },
  },
]
