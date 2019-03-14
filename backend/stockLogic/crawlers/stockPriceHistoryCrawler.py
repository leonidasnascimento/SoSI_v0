import sys
import time
import threading
import re
import locale

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\var\\www\\git\\sosi\\backend")

from dateutil import parser
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from helpers.parser import Parser
from helpers.web import Web
from models.stockPriceHistoryModel import StockPriceHistoryModel
from models.stockPriceDataModel import StockPriceDataModel

## GLOBAL
URL_YAHOO = "https://br.financas.yahoo.com/quote/{0}.SA/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d"

class StockPriceHistoryCrawler(StockPriceHistoryModel):
    def __init__(self, stockCode, periodInDays):
        self.StockCode = stockCode
        self.ListData = []
        self.__setStockPriceHistory(stockCode, periodInDays)
        
        pass

    def __setStockPriceHistory(self, stockCode, periodInDays):
        if stockCode is None or stockCode == "": return
        if periodInDays == 0: 
            periodInDays = 1
        
        locale.setlocale(locale.LC_ALL, 'pt_BR')

        period1 = date.today() - relativedelta(days=periodInDays)
        period2 = date.today()
        formatted_p1 = int(time.mktime(period1.timetuple()))
        formatted_p2 = int(time.mktime(period2.timetuple()))
        url_formatted = URL_YAHOO.format(stockCode, str(formatted_p1), str(formatted_p2))

        page = Web.GetWebPage(url_formatted)
        if (page is None): return

        lines = page.find_all("tr", class_="BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)")
        if (lines is None): return

        for line in lines:
            dateCell = line.find("td", class_="Py(10px) Ta(start) Pend(10px)").find("span").get_text()
            valuesCell = line.find_all("td", class_="Py(10px) Pstart(10px)")

            if valuesCell is None: continue
            if len(valuesCell) < 6: continue

            v1 = ""
            v2 = ""
            v3 = ""
            v4 = ""
            v5 = ""
            v6 = ""

            if not (valuesCell[0].find("span") is None):
                v1 = valuesCell[0].find("span").get_text()

            if not (valuesCell[1].find("span") is None):
                v2 = valuesCell[1].find("span").get_text()

            if not (valuesCell[2].find("span") is None):
                v3 = valuesCell[2].find("span").get_text()

            if not (valuesCell[3].find("span") is None):
                v4 = valuesCell[3].find("span").get_text()

            if not (valuesCell[4].find("span") is None):
                v5 = valuesCell[4].find("span").get_text()

            if not (valuesCell[5].find("span") is None):
                v6 = valuesCell[5].find("span").get_text()

            dateVal = datetime.strptime(dateCell, "%d de %b de %Y")
            openig = Parser.ParseFloat(v1)
            high = Parser.ParseFloat(v2)
            low = Parser.ParseFloat(v3)
            closing = Parser.ParseFloat(v4)
            adjusted = Parser.ParseFloat(v5)
            volume = Parser.ParseFloat(v6)

            self.AddStockPrice(high, low, openig, closing, adjusted, volume, dateVal)        
        pass
    pass