import sys
import time
import threading

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from helpers.web import Web
from helpers.parser import Parser
from datetime import datetime
from dateutil import parser

#############################
##                         ##
## STOCK SPECIALIZED CLASS ##
##                         ##
#############################

class StockCrawler(object):
    AvailableStockCode = None

    ## CONSTANTS ##
    MAIN_URL = "http://www.fundamentus.com.br/%s"
    DIVIDEND_URL = "http://www.fundamentus.com.br/proventos.php?papel=%s&tipo=2"

    def __init__(self, stockTypeFilter: ""):
        self.AvailableStockCode = self.GetAvailableStocks(stockTypeFilter)

    def GetAvailableStocks(self, stockTypeFilter):
        __availableStocksSingleton = None

        urlAux = self.MAIN_URL % "detalhes.php/"
        stocksPage = Web.GetWebPage(urlAux)

        if stocksPage is None:
            return __availableStocksSingleton

        stocksTbl = stocksPage.findChildren("table")

        if len(stocksTbl) == 0:
            return __availableStocksSingleton

        stocksRow = stocksTbl[0].findChildren("tr")

        if len(stocksRow) == 0:
            return __availableStocksSingleton

        for row in stocksRow:
            if row is None:
                continue

            columns = row.findChildren("td")

            if columns is None or len(columns) != 3:
                continue

            __availableStocksSingleton = __availableStocksSingleton if __availableStocksSingleton is not None else []
            stockAux = {}
            det = columns[0].findChildren("a")
            companyName = "%s - %s" % (columns[1].get_text(),
                                       columns[2].get_text())

            if (det is not None) and len(det) > 0:
                stockDetails = str(det[0].attrs["href"]).rstrip(
                    None).lstrip(None)
            else:
                continue

            stockCode = str(det[0].get_text()).rstrip(None)

            # STOCK FILTERING
            if stockTypeFilter != "":
                if stockTypeFilter.lower() == "on":
                    if (str(stockCode).find("3") < 0):
                        continue
                if stockTypeFilter.lower() == "pn":
                    if (str(stockCode).find("4") < 0):
                        continue

            # APPENDING ITEMS
            stockAux["stockCode"] = stockCode
            stockAux["stockDetails"] = stockDetails
            stockAux["companyName"] = companyName

            __availableStocksSingleton.append(stockAux)

        return __availableStocksSingleton
        # return [x for x in __availableStocksSingleton if (x["stockCode"] == "ITUB3" or x["stockCode"] == "BBDC3" or x["stockCode"] == "CSAN3")]

    def PrintProgress(self, actual, target):
        print(float((actual/target)*100).__round__(2))