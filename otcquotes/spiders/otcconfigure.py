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
X:xpath
'''

OTC_SITES_OK = [
  { 'name'                      : 'TianJin Equity Exchange',
    'homepage'                  : 'http://www.tjsoc.com/',
    'shortname'                 : 'tj',
    'startpage'                 : 1,
    'endpage'                   : 1,
    'quotes_url'                : 'http://www.tjsoc.com/web/homepage.aspx?name=schq',
    'stock_format'              : '//table[@id="ContentPlaceHolder1_GridView1"]//tr[@onclick]',
    'stockid_format'            : ['./@onclick', 'code=', '\''],
# in html it is <table style="..."><tr><td>, but it change to <table><tr><td><font>
    'stockname_format'          : './td[1]/font/text()',
    'stocknewprice_format'      : './td[2]/font/text()',
    'stocktotalamount_format'   : './td[3]/font/text()',
    'stock_url'                 : 'http://www.tjsoc.com/web/seksun.aspx?code={stockid}',
    'd_stock_format'            : '//div[@class="mainbox"]//table',
    'd_stocknumber_format'      : './tr[2]/td[2]/span/text()',
    'd_stockfullname_format'    : './tr[3]/td[2]/span/text()',
    'd_stockstart_format'       : './tr[4]/td[2]/span/text()',
    'd_stockweb_format'         : './tr[7]/td[2]/a/text()',
  },
  { 'name'                      : 'ShangHai Equity Exchange',
    'homepage'                  : 'http://www.china-see.com/stockInfo.do',
    'shortname'                 : 'sh',
    'startpage'                 : 1,
    'endpage'                   : '//div[@id="dropdown3"]/ul/li[last()]/a/text()',
    'quotes_url'                : 'http://www.china-see.com/stockInfo.do?pageNo={pagenum}',
    'stock_format'              : '//div[@class="wrap1Rsub"]//table/tr',
    'stockid_format'            : './td[1]/text()',
#    'stock_length_start'        : 0,
#    'stock_length_end'          : 6,
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
  { 'name'                      : 'AnHui Equity Exchange',
    'homepage'                  : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005',
    'shortname'                 : 'ah',
    'startpage'                 : 1,
    'endpage'                   : '//div[@class="page"]/font/text()',
    'quotes_url'                : 'http://www.ahsgq.com/aee/hqsj/qysj.jsp?classid=000100060005&pageno={pagenum}&pagesize=10',
    'stock_format'              : '//table[@class="tab03"]/tr',
    'stockid_format'            : './td[1]/span/a/@href',
#    'stock_length_start'        : 0,
#    'stock_length_end'          : 1000,           # means all
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

OTC_SITES = [
  { 'name'                      : 'Qilu Equity Exchange',
    'homepage'                  : 'http://www.zbotc.com/hangqing-guapai-list.php',
    'shortname'                 : 'zb',
    'startpage'                 : 1,
    'endpage'                   : ['//td[@width="153"]/div/text()', '/', ')'],
#    'endpage'                   : 'X://div[@id="dropdown3"]/ul/li[last()]/a/text()',
    'quotes_url'                : 'http://www.zbotc.com/hangqing-guapai-list.php?page={pagenum}',
    'stock_format'              : '//table[@id="Table41"//table/tr[@height="32"]',
    'stockid_format'            : './td[2]/a/text()',
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

OTC_SITES_after = [ 

  { 'name'                      : 'TianJin Equity Exchange',
    'homepage'                  : 'http://www.tjsoc.com/',
    'shortname'                 : 'tj',
    'startpage'                 : 1,
    'endpage'                   : 1,
    'quotes_url'                : 'http://www.tjsoc.com/web/homepage.aspx?name=schq',
    'stock_format'              : '//table[@id="ContentPlaceHolder1_GridView1"]//tr[@onclick]',
    'stockid_format'            : 'X:./@onclick',
    'stockid_format_s'          : 'S:code=',
    'stockid_format_e'          : 'E:\'',
# in html it is <table style="..."><tr><td>, but it change to <table><tr><td><font>
    'stockname_format'          : './td[1]/font/text()',
    'stocknewprice_format'      : './td[2]/font/text()',
    'stocktotalamount_format'   : './td[3]/font/text()',
    'stock_url'                 : 'http://www.tjsoc.com/web/seksun.aspx?code={stockid}',
    'd_stock_format'            : '//div[@class="mainbox"]//table',
    'd_stocknumber_format'      : './tr[2]/td[2]/span/text()',
    'd_stockfullname_format'    : './tr[3]/td[2]/span/text()',
    'd_stockstart_format'       : './tr[4]/td[2]/span/text()',
    'd_stockweb_format'         : './tr[7]/td[2]/a/text()',
  },

]

