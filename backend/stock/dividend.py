import sys
import urllib, json, pprint
from models.dividendModel import DividendModel
from helpers.parser import Parser

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
                dividendModelAux = DividendModel()
                dividendModelAux.Code = stock["code"]
                dividendModelAux.Company = stock["name"]
                dividendModelAux.Type = stock[FIELD_TYPE]
                dividendModelAux.StockPrice = Parser.ParseFloat(stock["price"]) 
                dividendModelAux.Sector = stock["sector"]
                dividendModelAux.Equity = Parser.ParseFloat(stock["equity"])       
                returnObj.append(dividendModelAux)
        return returnObj

def getStocksJson():
        # return open("C:\git\SoSI\backend\stock\mock\dividendMock.json", 'r') # Mock for tests
        return urllib.request.urlopen(SERVICE_ENDPOINT) # Production

stocks = json.load(getStocksJson())
filteredStocks = filterStocks(stocks, STOCK_TYPE_TO_FILTER)
divdendObj = getDividendModel(filteredStocks)
