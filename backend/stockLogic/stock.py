import sys
import requests
import urllib

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from bs4 import BeautifulSoup
from helpers.parser import Parser

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
        print("BOVESPA offered amount by stock successfully acquired!")

    def GetAvailableStocks(self):
        __availableStocksSingleton = None

        urlAux = self.MAIN_URL % "detalhes.php/"
        htmlPage = urllib.request.urlopen(urlAux)
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

            if columns is None or len(columns) != 3:
                continue

            __availableStocksSingleton = __availableStocksSingleton if __availableStocksSingleton is not None else []
            stockAux = {}
            det = columns[0].findChildren("a")
            companyName = "%s - %s" % (columns[1].get_text(), columns[2].get_text()) 
            
            if (det is not None) and len(det) > 0:
                stockDetails = str(det[0].attrs["href"]).rstrip(None).lstrip(None)
            else:
                continue
            
            stockCode = str(det[0].get_text()).rstrip(None)

            ## APPENDING ITEMS
            stockAux["stockCode"] = stockCode
            stockAux["stockDetails"] = stockDetails
            stockAux["companyName"] = companyName

            __availableStocksSingleton.append(stockAux)

        return __availableStocksSingleton

    def GetStocksBasicInfo(self):
        returnList = []
        stockBasicInfoList = {}

        if (len(self.AvailableStockCode) == 0):
            self.AvailableStockCode = self.GetAvailableStocks()

        for stock in self.AvailableStockCode:       
            urllib.request.urlcleanup()
            htmlPage = urllib.request.urlopen(self.MAIN_URL % stock["stockDetails"])
            stocksPage = BeautifulSoup(htmlPage.read(), features="html.parser")

            if stocksPage is None: return None

            stocksTbl = stocksPage.findChildren("table")

            if (stocksTbl is None) or (len(stocksTbl) != 5): continue

            ## START -- REGISTRATION INFO
            if (stocksTbl[0].contents is None) or (len(stocksTbl[0].contents) != 11): continue
       
            #### PRICE
            if (stocksTbl[0].contents[1].contents is None) or (len(stocksTbl[0].contents[1].contents) != 9): continue
            stockPrice = stocksTbl[0].contents[1].contents[7].get_text()
       
            #### TYPE
            if (stocksTbl[0].contents[3].contents is None) or (len(stocksTbl[0].contents[3].contents) != 9): continue
            stockType = stocksTbl[0].contents[3].contents[3].get_text()

            #### PRIMARY SECTOR
            if (stocksTbl[0].contents[7].contents is None) or (len(stocksTbl[0].contents[7].contents) != 9): continue
            primarySector = stocksTbl[0].contents[7].contents[3].get_text()

            #### SECONDARY SECTOR
            if (stocksTbl[0].contents[9].contents is None) or (len(stocksTbl[0].contents[9].contents) != 9): continue
            secondarySector = stocksTbl[0].contents[9].contents[3].get_text()

            ## END -- REGISTRATION INFO

            ## POPULATING THE RESULT LIST
            stockBasicInfoList["stock"] = stock["stockCode"]
            stockBasicInfoList["stockType"] = "ON" if str(stockType).upper().find("ON") == 0 else "PN"
            stockBasicInfoList["stockPrice"] = Parser.ParseFloat(stockPrice)
            stockBasicInfoList["primarySector"] = str(primarySector).rstrip(None).lstrip(None)
            stockBasicInfoList["secondarySector"] = str(secondarySector).rstrip(None).lstrip(None)

            returnList.append(stockBasicInfoList)

        return returnList

            