import sys
import time
import threading
import re

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import date
from helpers.parser import Parser
from helpers.web import Web
from models.dividendHistoryModel import DividendHistoryModel
from models.dividendDataModel import DividendDataModel

## GLOBAL
URL_YAHOO = "https://br.financas.yahoo.com/quote/{0}.SA/history?period1={1}&period2={2}&interval=div%7Csplit&filter=div&frequency=1d"

class DividendHistoryCrawler(DividendHistoryModel):
    def __init__(self, stockCode, periodInMonths):
        self.StockCode = stockCode
        self.ListData = []

        self.SetDividends(stockCode, periodInMonths)

    def SetDividends(self, stockCode, periodInMonths):
        if stockCode is None or stockCode == "": return
        if periodInMonths == 0: 
            periodInMonths = 1
        
        period1 = date.today() - relativedelta(months=periodInMonths)
        period2 = date.today()
        formatted_p1 = int(time.mktime(period1.timetuple()))
        formatted_p2 = int(time.mktime(period2.timetuple()))
        url_formatted = URL_YAHOO.format(stockCode, str(formatted_p1), str(formatted_p2))

        page = Web.GetWebPage(url_formatted)
        if (page is None): return

        pass