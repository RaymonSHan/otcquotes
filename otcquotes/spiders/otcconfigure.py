# -*- coding:gbk -*-
#
# Althought I do not input any Chinese in my project, I still insert this progma before any codes.
# Recommen GBK instead of Unicode or UTF-8 in any case.
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

STOCKNAME                       = 'StockName'
STOCKFULLNAME                   = 'StockFullName'
STOCKNUMBER                     = 'StockNumber'
STOCKNEWPRICE                   = 'StockNewPrice'
STOCKTOTALAMOUNT                = 'StockTotalAmount'
STOCKOPENDATE                   = 'StockOpenDate'
STOCKHOMEPAGE                   = 'StockHomePage'

STOCKINFOURL                    = 'StockInfoURL'

OTC_SITES = [
  { FULLNAME                    : 'TianJin Equity Exchange',
    HOMEPAGE_URL                : 'http://www.tjsoc.com/',
    ABBRNAME                    : 'tj',
    PAGESTART                   : 1,
    PAGEEND                     : 1,
    ONEPAGE_URL                 : 'http://www.tjsoc.com/web/homepage.aspx?name=schq',
    ONESTOCK_FORMAT             : '//table[@id="ContentPlaceHolder1_GridView1"]//tr[@onclick]',
    ONESTOCKID                  : ['./@onclick', 'code=', '\''],
# in html it is <table style="..."><tr><td>, but it change to <table><tr><td><font>
      LISTPAGEDETAIL            : {
        STOCKNAME               : './td[1]/font/text()',
        STOCKNEWPRICE           : './td[2]/font/text()',
        STOCKTOTALAMOUNT        : './td[3]/font/text()',
       },
    DETAILSTOCK_URL             : 'http://www.tjsoc.com/web/seksun.aspx?code={stockid}',
    DETAILSTOCK_FORMAT          : '//div[@class="mainbox"]//table',
      STOCKPAGEDETAIL           : {
        STOCKNUMBER             : './tr[2]/td[2]/span/text()',
        STOCKFULLNAME           : './tr[3]/td[2]/span/text()',
        STOCKOPENDATE           : './tr[4]/td[2]/span/text()',
        STOCKHOMEPAGE           : './tr[7]/td[2]/a/text()',
      },
    },
  ]
'''
    'stockname_format'          : 
    'stocknewprice_format'      : 
    'stocktotalamount_format'   : 
    'stock_url'                 : 
    'd_stock_format'            : 
    'd_stocknumber_format'      : 
    'd_stockfullname_format'    : 
    'd_stockstart_format'       : 
    'd_stockweb_format'         : 
'''
OTC_OLD_OK = [
  { FULLNAME                    : 'ShangHai Equity Exchange',
    HOMEPAGE_URL                : 'http://www.china-see.com/stockInfo.do',
    ABBRNAME                    : 'sh',
    PAGESTART                   : 1,
    PAGEEND                     : '//div[@id="dropdown3"]/ul/li[last()]/a/text()',
    ONEPAGE_URL                 : 'http://www.china-see.com/stockInfo.do?pageNo={pagenum}',
    ONESTOCK_FORMAT             : '//div[@class="wrap1Rsub"]//table/tr',
    ONESTOCKID                  : './td[1]/text()',
    'stockname_format'          : './td[2]/text()',
    'stocknewprice_format'      : './td[3]/text()',
    'stocktotalamount_format'   : './td[13]/div/text()',
    'stock_url'                 : 'http://www.china-see.com/f10.do?tabIndex=1&stockCode={stockid}',
    'd_stock_format'            : '//div[@class="tabcon"]/table',
    'd_stocknumber_format'      : './tr[4]/td[1]/text()',
    'd_stockfullname_format'    : './tr[1]/td[1]/text()',
    'd_stockstart_format'       : './tr[9]/td[1]/text()',
    'd_stockweb_format'         : './tr[13]/td[1]/text()',
  },
  { FULLNAME                    : 'AnHui Equity Exchange',
    HOMEPAGE_URL                : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005',
    ABBRNAME                    : 'ah',
    PAGESTART                   : 1,
    PAGEEND                     : '//div[@class="page"]/font/text()',
    ONEPAGE_URL                 : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005&pageno={pagenum}&pagesize=10',
    ONESTOCK_FORMAT             : '//table[@class="tab03"]/tr',
    ONESTOCKID                  : './td[1]/span/a/@href',
    'stockname_format'          : './td[2]/a/text()',
    'stocknewprice_format'      : './td[3]/span/text()',
    'stocktodaymount_format'    : './td[4]/text()',
#    'stocktotalamount_format'   : '',
    'stock_url'                 : 'http://www.ahsgq.com{stockid}',
    'd_stock_format'            : '//table[@class="tab05"]',
    'd_stocknumber_format'      : './tr[3]/td[1]/text()',
    'd_stockfullname_format'    : './tr[1]/td[1]/text()',
    'd_stockstart_format'       : './tr[7]/td[1]/text()',
    'd_stockweb_format'         : './tr[11]/td[1]/text()',
  },
]

OTC_SITES__ = [
  { FULLNAME                    : 'Qilu Equity Exchange',
    HOMEPAGE_URL                : 'http://www.zbotc.com/hangqing-guapai-list.php',
    ABBRNAME                    : 'zb',
    PAGESTART                   : 1,
    PAGEEND                     : ['//td[@width="153"]/div/text()', '/', ')'],
    ONEPAGE_URL                 : 'http://www.zbotc.com/hangqing-guapai-list.php?page={pagenum}',
    ONESTOCK_FORMAT             : '//table[@id="Table41"//table/tr[@height="32"]',
    ONESTOCKID                  : './td[2]/a/text()',
    'stockname_format'          : './td[3]/a/text()',
    'stocknewprice_format'      : './td[3]/text()',
    'stocktotalamount_format'   : './td[13]/div/text()',
    'stock_url'                 : 'http://www.china-see.com/f10.do?tabIndex=1&stockCode={stockid}',
    'd_stock_format'            : '//div[@class="tabcon"]/table',
    'd_stocknumber_format'      : './tr[4]/td[1]/text()',
    'd_stockfullname_format'    : './tr[1]/td[1]/text()',
    'd_stockstart_format'       : './tr[9]/td[1]/text()',
    'd_stockweb_format'         : './tr[13]/td[1]/text()',
  },
]
