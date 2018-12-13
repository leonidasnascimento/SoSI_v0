import sys
import requests
import urllib
from bs4 import BeautifulSoup

#############################
##                         ##   
## STOCK SPECIALIZED CLASS ##
##                         ##
#############################
class Stock(object):
    AvailableStockCode = None
    StocksBasicInfo = None
    
    ## CONSTANTS ##
    MAIN_URL = "http://www.fundamentus.com.br/%s"

    def __init__ (self):
        self.AvailableStockCode = self.GetAvailableStocks()
        print("BOVESPA available stocks successfully acquired!")
        self.StocksBasicInfo = self.GetStocksBasicInfo()
        print("BOVESPA stocks offered amount successfully acquired!")

    def GetAvailableStocks(self):
        __availableStocksSingleton = None

        htmlPage = urllib.request.urlopen(self.MAIN_URL % "detalhes.php")
        stocksPage = BeautifulSoup(htmlPage.read(), features="html.parser")

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

            if columns is None or len(columns) == 0:
                continue

            __availableStocksSingleton = __availableStocksSingleton if __availableStocksSingleton is not None else []
            det = columns[0].findChildren("a")

            stockAux = []

            if (det is not None) and len(det) > 0:
                stockAux.append(str(det[0].attrs["href"]).rstrip(None))
            else:
                continue
            
            stockAux.append(str(det[0].get_text()).rstrip(None))

            __availableStocksSingleton.append(stockAux)

        return __availableStocksSingleton

    def GetStocksBasicInfo(self):
        if (len(self.AvailableStockCode) == 0):
            self.AvailableStockCode = self.GetAvailableStocks()

        for stock in self.AvailableStockCode:
            htmlPage = urllib.request.urlopen(self.MAIN_URL % stock[0])
            stocksPage = BeautifulSoup(htmlPage.read(), features="html.parser")

            if stocksPage is None:
                return None

            stocksTbl = stocksPage.findChildren("table")
