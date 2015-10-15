# -*- coding:gbk -*-
#
# Althought I do not input any Chinese in my project, I still insert this progma before any codes.
# Recommen GBK instead of Unicode or UTF-8 in any case.
#
# Wrapping Column 132.
import otcquotes

'''
S:key
E:key
'''
OTC_SITES = [ 
  { 'name'                      : 'ShangHai Equity Exchange',
    'homepage'                  : 'http://www.china-see.com/stockInfo.do',
    'shortname'                 : 'sh',
    'startpage'                 : 1,
    'endpage'                   : 1,
#    'endpage'                   : 'X://div[@id="dropdown3"]/ul/li[last()]',
    'quotes_url'                : 'http://www.china-see.com/stockInfo.do?pageNo={pagenum}',
    'stock_format'              : '//div[@class="wrap1Rsub"]//table/tr',
    'stockid_format'            : './td[1]/text()',
    'stock_length_start'        : 0,
    'stock_length_end'          : 6,
    'stockname_format'          : './td[2]',
    'stocknewprice_format'      : './td[3]',
    'stocktotalamount_format'   : './td[13]/div',
    'stock_url'                 : 'http://www.china-see.com/f10.do?tabIndex=1&stockCode={stockid}',
    'd_stock_format'            : '//div[@class="tabcon"]/table',
    'd_stocknumber_format'      : './tr[4]/td[1]',
    'd_stockfullname_format'    : './tr[1]/td[1]',
    'd_stockstart_format'       : './tr[9]/td[1]',
    'd_stockweb_format'         : './tr[13]/td[1]',
  },]



OTC_SITES_OK = [ 
  { 'name'                      : 'TianJin Equity Exchange',
    'homepage'                  : 'http://www.tjsoc.com/',
    'shortname'                 : 'tj',
    'startpage'                 : 1,
    'endpage'                   : 1,
    'quotes_url'                : 'http://www.tjsoc.com/web/homepage.aspx?name=schq',
    'stock_format'              : '//table[@id="ContentPlaceHolder1_GridView1"]//tr[@onclick]',
    'stockid_format'            : './@onclick',
    'stock_length_start'        : 'S:code=',
    'stock_length_end'          : 'E:\'',
# in html it is <table style="..."><tr><td>, but it change to <table><tr><td><font>
    'stockname_format'          : './td[1]/font',
    'stocknewprice_format'      : './td[2]/font',
    'stocktotalamount_format'   : './td[3]/font',
    'stock_url'                 : 'http://www.tjsoc.com/web/seksun.aspx?code={stockid}',
    'd_stock_format'            : '//div[@class="mainbox"]//table',
    'd_stocknumber_format'      : './tr[2]/td[2]/span',
    'd_stockfullname_format'    : './tr[3]/td[2]/span',
    'd_stockstart_format'       : './tr[4]/td[2]/span',
    'd_stockweb_format'         : './tr[7]/td[2]/a',
  },
  { 'name'                      : 'ShangHai Equity Exchange',
    'homepage'                  : 'http://www.china-see.com/stockInfo.do',
    'shortname'                 : 'sh',
    'startpage'                 : 1,
    'endpage'                   : 'X://div[@id="dropdown3"]/ul/li[last()]',
    'quotes_url'                : 'http://www.china-see.com/stockInfo.do?pageNo={pagenum}',
    'stock_format'              : '//div[@class="wrap1Rsub"]//table/tr',
    'stockid_format'            : './td[1]/text()',
    'stock_length_start'        : 0,
    'stock_length_end'          : 6,
    'stockname_format'          : './td[2]',
    'stocknewprice_format'      : './td[3]',
    'stocktotalamount_format'   : './td[13]/div',
    'stock_url'                 : 'http://www.china-see.com/f10.do?tabIndex=1&stockCode={stockid}',
    'd_stock_format'            : '//div[@class="tabcon"]/table',
    'd_stocknumber_format'      : './tr[4]/td[1]',
    'd_stockfullname_format'    : './tr[1]/td[1]',
    'd_stockstart_format'       : './tr[9]/td[1]',
    'd_stockweb_format'         : './tr[13]/td[1]',
  },
]
