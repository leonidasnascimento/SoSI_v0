import sys
import requests
import urllib
import time
import threading
import datetime

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from bs4 import BeautifulSoup
from helpers.parser import Parser
from datetime import datetime
from dateutil import parser 

#############################
##                         ##   
## STOCK SPECIALIZED CLASS ##
##                         ##
#############################
class Stock(object):
    AvailableStockCode = None
    StocksBasicInfo = None
    DividendsData = None
    
    ## CONSTANTS ##
    MAIN_URL = "http://www.fundamentus.com.br/%s"
    DIVIDEND_URL = "http://www.fundamentus.com.br/proventos.php?papel=%s&tipo=2"

    def __init__ (self, stockTypeFilter: ""):
        threads = []
        tasks = [
            self.GetDividendData,
            # self.GetStocksBasicInfo
        ]

        self.AvailableStockCode = self.GetAvailableStocks(stockTypeFilter)

        # Queueing tasks 
        for task in tasks:
            threads.append(threading.Thread(target=task))

        # Executing tasks
        for thread in threads:
            thread.start()

        # Waiting all threads to be completed
        for thread in threads:
            thread.join()

    def GetAvailableStocks(self, stockTypeFilter):
        __availableStocksSingleton = None

        urlAux = self.MAIN_URL % "detalhes.php/"
        stocksPage = self.GetWebPage(urlAux)

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

            ### STOCK FILTERING
            if stockTypeFilter != "":
                if stockTypeFilter.lower() == "on":
                    if (str(stockCode).find("3") < 0): continue
                if stockTypeFilter.lower() == "pn":
                    if (str(stockCode).find("4") < 0): continue
            
            ## APPENDING ITEMS
            stockAux["stockCode"] = stockCode
            stockAux["stockDetails"] = stockDetails
            stockAux["companyName"] = companyName

            __availableStocksSingleton.append(stockAux)

        return __availableStocksSingleton

    def GetStocksBasicInfo(self):
        self.StocksBasicInfo = []
        stockBasicInfoList = {}
        counter = 0    

        if (len(self.AvailableStockCode) == 0):
            self.AvailableStockCode = self.GetAvailableStocks()

        for stock in self.AvailableStockCode:       
            # self.PrintProgress(counter, len(self.AvailableStockCode))
            
            stocksPage = self.GetWebPage(self.MAIN_URL % stock["stockDetails"])

            if stocksPage is None: return None

            stocksTbl = stocksPage.findChildren("table")

            if (stocksTbl is None) or (len(stocksTbl) != 5): continue

            ## REGISTRATION INFO
            if (stocksTbl[0].contents is not None) and (len(stocksTbl[0].contents) == 11):
            
                #### PRICE
                if (stocksTbl[0].contents[1].contents is not None) and (len(stocksTbl[0].contents[1].contents) == 9):
                    stockPrice = stocksTbl[0].contents[1].contents[7].get_text()
        
                #### TYPE
                if (stocksTbl[0].contents[3].contents is not None) and (len(stocksTbl[0].contents[3].contents) == 9):
                    stockType = stocksTbl[0].contents[3].contents[3].get_text()

                #### PRIMARY SECTOR
                if (stocksTbl[0].contents[7].contents is not None) and (len(stocksTbl[0].contents[7].contents) == 9):
                    primarySector = stocksTbl[0].contents[7].contents[3].get_text()

                #### SECONDARY SECTOR
                if (stocksTbl[0].contents[9].contents is not None) and (len(stocksTbl[0].contents[9].contents) == 9):
                    secondarySector = stocksTbl[0].contents[9].contents[3].get_text()

                #### AVG NEGOCIATION VOLUME
                if (stocksTbl[0].contents[9].contents is not None) and (len(stocksTbl[0].contents[9].contents) == 9):
                    avgNegociationValue = stocksTbl[0].contents[9].contents[7].get_text()

            ## END - REGISTRATION INFO

            ## MKT INFORMATION
            if (stocksTbl[1].contents is not None) and (len(stocksTbl[1].contents) == 5):

                #### MKT VALUE
                if (stocksTbl[1].contents[1].contents is not None) and (len(stocksTbl[1].contents[1].contents) == 9):
                    mktValue = stocksTbl[1].contents[1].contents[3].get_text()

                #### STOCK AMOUNT
                if (stocksTbl[1].contents[3].contents is not None) and (len(stocksTbl[1].contents[3].contents) == 9):
                    stockAmount = stocksTbl[1].contents[3].contents[7].get_text()
            
            ## PROFIT
            if (stocksTbl[4].contents is not None) and (len(stocksTbl[4].contents) == 11):
                
                #### NET PROFIT
                if (stocksTbl[4].contents[9].contents is not None) and (len(stocksTbl[4].contents[9].contents) == 9):
                    netProfit = stocksTbl[4].contents[9].contents[3].get_text()
            ## END - MKT INFORMATION

            ## POPULATING THE RESULT LIST
            stockBasicInfoList["stock"] = stock["stockCode"]
            stockBasicInfoList["stockType"] = "ON" if str(stockType).upper().find("ON") == 0 else "PN"
            stockBasicInfoList["stockPrice"] = Parser.ParseFloat(stockPrice)
            stockBasicInfoList["primarySector"] = str(primarySector).rstrip(None).lstrip(None)
            stockBasicInfoList["secondarySector"] = str(secondarySector).rstrip(None).lstrip(None)
            stockBasicInfoList["avgNegociationValue"] = Parser.ParseFloat(avgNegociationValue)
            stockBasicInfoList["mktValue"] = Parser.ParseFloat(mktValue)
            stockBasicInfoList["stockAmount"] = Parser.ParseFloat(stockAmount)
            stockBasicInfoList["netProfit"] = Parser.ParseFloat(netProfit)

            self.StocksBasicInfo.append(stockBasicInfoList)
            counter += 1

    def GetDividendData(self):
        stocks = {}
        self.DividendData = []
        dividendRowCounter = -1

        if(self.AvailableStockCode is None): return None
        
        for stock in self.AvailableStockCode:

            stocksPage = self.GetWebPage(self.DIVIDEND_URL % "ITUB4")# stock["stockCode"])
            if(stocksPage is None): continue
        
            stocksTbl = stocksPage.findChildren("table")
            if (stocksTbl is None) or (len(stocksTbl) != 1): continue

            dividendTbl = stocksTbl[0].contents 
            if (dividendTbl is None) or (len(dividendTbl) != 5): continue

            dividendRows = dividendTbl[3]
            if (dividendTbl is None): continue
            
            stocks["stockCode"] = stock["stockCode"]
            stocks["dividends"] = []   

            for row in dividendRows:                
                dividendRowCounter += 1

                if (dividendRowCounter % 2 == 0): continue
                if len(row.contents) != 9: continue
                if row.contents[5].get_text().lower().find("dividend") < 0: continue
                
                dateAux = datetime.strptime(row.contents[1].get_text(), "%d/%m/%Y").strftime("%Y-%m-%d")
                # For performance reason, only two years are returned
                if (datetime.today().year - datetime.strptime(dateAux, "%Y-%m-%d").year) > 2: break 
                
                dataAux = {}
                dataAux["date"] = dateAux
                dataAux["value"] = Parser.ParseFloat(row.contents[3].get_text())

                stocks["dividends"].append(dateAux)    

            self.DividendData.append(stocks)
            break

    def GetWebPage(self, url):
        success = False
    
        while(not success):
            try:
                urllib.request.urlcleanup()
                htmlPage = urllib.request.urlopen(url)
                stocksPage = BeautifulSoup(htmlPage.read(), features="html.parser")
                success = True
            except Exception:
                time.sleep(5)    
                continue

        return stocksPage
    
    def PrintProgress(self, actual, target):
        print(float((actual/target)*100).__round__(2))