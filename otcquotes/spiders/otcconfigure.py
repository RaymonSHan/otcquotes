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
    'stockname_format'          : './td[1]',
    'stocknewprice_format'      : './td[2]',
    'stocktotalamount_format'   : './td[3]',
    'stock_url'                 : 'http://www.tjsoc.com/web/seksun.aspx?code={stockid}',
  },
  { 'name'                      : 'ShangHai Equity Exchange',
    'homepage'                  : 'http://www.china-see.com/',
    'shortname'                 : 'sh',
    'startpage'                 : 1,
    'endpage'                   : 2,
    'quotes_url'                : 'http://www.china-see.com/stockInfo.do?pageNo={pagenum}',
    'stock_format'              : '',
    'stock_url'                 : '',
  },]

