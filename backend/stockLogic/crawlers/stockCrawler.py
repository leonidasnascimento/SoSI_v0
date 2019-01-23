import sys
import time
import threading

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from dateutil import parser
from datetime import datetime
from helpers.parser import Parser
from helpers.web import Web


#############################
##                         ##
## STOCK SPECIALIZED CLASS ##
##                         ##
#############################


class StockCrawler(object):
    AvailableStockCode = None
    StocksBasicInfo = None
    DividendsData = None

    ## CONSTANTS ##
    MAIN_URL = "http://www.fundamentus.com.br/%s"
    DIVIDEND_URL = "http://www.fundamentus.com.br/proventos.php?papel=%s&tipo=2"

    def __init__(self, stockTypeFilter: ""):
        threads = []
        tasks = [
            self.GetDividendData,
            self.GetStocksBasicInfo
        ]

        self.AvailableStockCode = self.GetAvailableStocks(stockTypeFilter)

        # Queueing tasks
        for task in tasks:
            threads.append(threading.Thread(target=task))

        self.ExecuteThread(threads)

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

    def GetStocksBasicInfo(self):
        self.StocksBasicInfo = []
        threads = []

        if (len(self.AvailableStockCode) == 0):
            return

        # Queueing the tasks
        for stock in self.AvailableStockCode:
            self.GetStocksBasicInfoThreading(stock["stockCode"], stock["stockDetails"])
            # threads.append(threading.Thread(target=self.GetStocksBasicInfoThreading, args=(stock["stockCode"], stock["stockDetails"],)))

        # self.ExecuteThread(threads)

    def GetStocksBasicInfoThreading(self, stockCode, stockDetailsPage):
        stockBasicInfoList = {}
        stocksPage = Web.GetWebPage(self.MAIN_URL % stockDetailsPage)
        if stocksPage is None: return
        
        stocksTbl = stocksPage.findChildren("table")
        if (stocksTbl is None) or (len(stocksTbl) != 5): return

        # REGISTRATION INFO
        if (stocksTbl[0].contents is not None) and (len(stocksTbl[0].contents) == 11):

            # PRICE
            if (stocksTbl[0].contents[1].contents is not None) and (len(stocksTbl[0].contents[1].contents) == 9):
                stockPrice = stocksTbl[0].contents[1].contents[7].get_text()

            # TYPE
            if (stocksTbl[0].contents[3].contents is not None) and (len(stocksTbl[0].contents[3].contents) == 9):
                stockType = stocksTbl[0].contents[3].contents[3].get_text()

            # PRIMARY SECTOR
            if (stocksTbl[0].contents[7].contents is not None) and (len(stocksTbl[0].contents[7].contents) == 9):
                primarySector = stocksTbl[0].contents[7].contents[3].get_text()

            # SECONDARY SECTOR
            if (stocksTbl[0].contents[9].contents is not None) and (len(stocksTbl[0].contents[9].contents) == 9):
                secondarySector = stocksTbl[0].contents[9].contents[3].get_text(
                )

            # AVG NEGOCIATION VOLUME
            if (stocksTbl[0].contents[9].contents is not None) and (len(stocksTbl[0].contents[9].contents) == 9):
                avgNegociationValue = stocksTbl[0].contents[9].contents[7].get_text(
                )

        # END - REGISTRATION INFO

        # MKT INFORMATION
        if (stocksTbl[1].contents is not None) and (len(stocksTbl[1].contents) == 5):

            # MKT VALUE
            if (stocksTbl[1].contents[1].contents is not None) and (len(stocksTbl[1].contents[1].contents) == 9):
                mktValue = stocksTbl[1].contents[1].contents[3].get_text()

            # STOCK AMOUNT
            if (stocksTbl[1].contents[3].contents is not None) and (len(stocksTbl[1].contents[3].contents) == 9):
                stockAmount = stocksTbl[1].contents[3].contents[7].get_text()

        # PROFIT
        if (stocksTbl[4].contents is not None) and (len(stocksTbl[4].contents) == 11):

            # NET PROFIT
            if (stocksTbl[4].contents[9].contents is not None) and (len(stocksTbl[4].contents[9].contents) == 9):
                netProfit = stocksTbl[4].contents[9].contents[3].get_text()
        # END - MKT INFORMATION

        # BALANCE SHEET
        if (stocksTbl[3].contents != None) and (len(stocksTbl[3].contents) == 9):

            # EQUITY
            if (stocksTbl[3].contents[7].contents != None) and (len(stocksTbl[3].contents[7].contents) == 9):
                equity = stocksTbl[3].contents[7].contents[7].get_text()
        # END - BALANCE SHEET

        # DIVIDENDS
        if (stocksTbl[2].contents != None) and (len(stocksTbl[2].contents) == 25):

            # DIVIDEND YELD
            if (stocksTbl[2].contents[17] != None) and (len(stocksTbl[2].contents[17]) == 13):            
                dividendYeld = stocksTbl[2].contents[17].contents[7].get_text()

        # LPA
        spanList = stocksPage.find_all('span', {'class' :'txt'})
        
        if not (spanList is None):
            lpaLabel = [l for l in spanList if str(l.text).lower() == "lpa"]
            if (not (lpaLabel is None)) or (len(lpaLabel) > 0):
                lpa = lpaLabel[0].parent.findNext('td').contents[0].get_text()

        # END - DIVIDENDS

        # POPULATING THE RESULT LIST
        stockBasicInfoList["stock"] = stockCode
        stockBasicInfoList["stockType"] = "ON" if str(
            stockType).upper().find("ON") == 0 else "PN"
        stockBasicInfoList["stockPrice"] = Parser.ParseFloat(stockPrice)
        stockBasicInfoList["primarySector"] = str(
            primarySector).rstrip(None).lstrip(None)
        stockBasicInfoList["secondarySector"] = str(
            secondarySector).rstrip(None).lstrip(None)
        stockBasicInfoList["avgNegociationValue"] = Parser.ParseFloat(
            avgNegociationValue)
        stockBasicInfoList["mktValue"] = Parser.ParseFloat(mktValue)
        stockBasicInfoList["stockAmount"] = Parser.ParseFloat(stockAmount)
        stockBasicInfoList["netProfit"] = Parser.ParseFloat(netProfit)
        stockBasicInfoList["equity"] = Parser.ParseFloat(equity)
        stockBasicInfoList["dividendYeld"] = Parser.ParseFloat(dividendYeld)
        stockBasicInfoList["lpa"] = Parser.ParseFloat(lpa)

        self.StocksBasicInfo.append(stockBasicInfoList)

    def GetDividendData(self):
        stocks = {}
        self.DividendsData = []
        dividendRowCounter = -1
        dividendRowRead = 0

        if(self.AvailableStockCode is None):
            return None

        for stock in self.AvailableStockCode:
            dividendRowCounter = -1
            dividendRowRead = 0

            stocksPage = Web.GetWebPage(
                self.DIVIDEND_URL % stock["stockCode"])
            if(stocksPage is None):
                continue

            stocksTbl = stocksPage.findChildren("table")
            if (stocksTbl is None) or (len(stocksTbl) != 1):
                continue

            dividendTbl = stocksTbl[0].contents
            if (dividendTbl is None) or (len(dividendTbl) != 5):
                continue

            dividendRows = dividendTbl[3]
            if (dividendTbl is None):
                continue

            stocks = {}    
            stocks["stockCode"] = stock["stockCode"]
            stocks["dividends"] = []

            for row in dividendRows:
                dividendRowCounter += 1

                if (dividendRowRead == 20): break
                if (dividendRowCounter % 2 == 0): continue
                if len(row.contents) != 9: continue
                if row.contents[5].get_text().lower().find("dividend") < 0: continue
                
                dividendRowRead += 1
                dateAux = row.contents[1].get_text()
                # dateAux = datetime.strptime(row.contents[1].get_text(), "%d/%m/%Y").strftime("%Y-%m-%d")

                stocks["dividends"].append({"date": dateAux, "dividend": Parser.ParseFloat(row.contents[3].get_text())})

            self.DividendsData.append(stocks)

    def PrintProgress(self, actual, target):
        print(float((actual/target)*100).__round__(2))

    def ExecuteThread(self, threads):
        # Threading the tasks
        for thread in threads:
            thread.start()

        # Waiting all threads to be completed
        for thread in threads:
            thread.join()