import urllib, json, pprint, sys

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from models.dividendModel import DividendModel
from helpers.parser import Parser
from database.dividendDb import DividendDb

### GLOBAL CONSTANTS ###
SERVICE_ENDPOINT = "https://www.bussoladoinvestidor.com.br/nb/api/v1/stocks"
STOCK_TYPE_TO_FILTER = "ON" # Leave it empty for all types

# FIELDS #
FIELD_RESULTS = "results"
FIELD_TYPE = "type"

# METHODS #
def FilterStocks(stocks, type):
        return [s for s in stocks[FIELD_RESULTS] if s[FIELD_TYPE] == type]

def GetDividendModel(stocks):
        returnObj = []
        for stock in stocks:
                dividendModelAux = DividendModel()
                dividendModelAux.Code = stock["code"]
                dividendModelAux.Company = stock["name"]
                dividendModelAux.Type = stock[FIELD_TYPE]
                dividendModelAux.StockPrice = Parser.ParseFloat(stock["price"]) 
                dividendModelAux.Sector = stock["sector"]
                dividendModelAux.Equity = Parser.ParseFloat(stock["equity"])
                dividendModelAux.Avarage21Negociation = 0
                dividendModelAux.AvgPayoutFiveYears = 0
                dividendModelAux.AvgPayoutTwelveMonths = 0
                dividendModelAux.DividendLastPrice = Parser.ParseFloat("")
                dividendModelAux.DividendPeriod = ""
                dividendModelAux.DividendTotalValueShared = 0.00
                dividendModelAux.DividendYeld = 0.00
                dividendModelAux.MajorShareholder = ""
                dividendModelAux.NetProfit = Parser.ParseFloat(stock["profit"])      
                returnObj.append(dividendModelAux)
        return returnObj

def GetStocksJson(strEndPoint):
        return open("C:\git\SoSI\\backend\stock\mock\dividendMock.json", "r") # Mock for tests
        # return urllib.request.urlopen(strEndPoint) # Production

def Save(lstDividend):
        for stock in stocks:
                if DividendDb().Save(stock) == False:
                        return False
        return True 

stocks = json.load(GetStocksJson(SERVICE_ENDPOINT))
filteredStocks = FilterStocks(stocks, STOCK_TYPE_TO_FILTER)
divdendObj = GetDividendModel(filteredStocks)

if Save(divdendObj) == False:
        raise SystemError()