import urllib, json, sys, pprint
from models.dividendModel import dividendModel

### GLOBAL CONSTANTS ###
SERVICE_ENDPOINT = "https://www.bussoladoinvestidor.com.br/nb/api/v1/stocks"
STOCK_TYPE_TO_FILTER = "ON" # Leave it empty for all types

# FIELDS #
FIELD_RESULTS = "results"
FIELD_TYPE = "type"

# METHODS #
def filterStocks(stocks, type):
        return [s for s in stocks[FIELD_RESULTS] if s[FIELD_TYPE] == type]

def getDividendModel(stocks):
        returnObj = []
        for stock in stocks:
                dividendModelAux = dividendModel()
                dividendModelAux.Code = stock["code"]
                dividendModelAux.Company = stock["name"]
                dividendModelAux.Type = stock[FIELD_TYPE]
                dividendModelAux.StockPrice = float(str(stock["price"]).replace(',', '.')) 
                dividendModelAux.Sector = stock["sector"]
                dividendModelAux.Equity = float(stock["equity"]) # float(str(stock["equity"]).replace(',', '.'))       
                returnObj.append(dividendModelAux)
        return returnObj

def getStocksJson():
        return open("C:\git\SoSI\backend\stock\mock\dividendMock.json", 'r') # Mock for tests
        # return urllib.request.urlopen(SERVICE_ENDPOINT) # Production

stocks = json.load(getStocksJson())
filteredStocks = filterStocks(stocks, STOCK_TYPE_TO_FILTER)
divdendObj = getDividendModel(filteredStocks)
