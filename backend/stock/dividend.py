import urllib, json, pprint, sys

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from models.dividendModel import DividendModel
from helpers.parser import Parser
from database.dividendDbCommand import DividendDbCommand

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
                dividendModelAux.SecondSector = ""
                dividendModelAux.Equity = Parser.ParseFloat(stock["equity"])
                dividendModelAux.Avg21Negociation = Parser.ParseFloat("")
                dividendModelAux.AvgPayout5Years = Parser.ParseFloat("")
                dividendModelAux.AvgPayout12Months = Parser.ParseFloat("")
                dividendModelAux.DividendLastPrice = Parser.ParseFloat("")
                dividendModelAux.DividendPeriod = 0
                dividendModelAux.DividendTotalValueShared = Parser.ParseFloat("")
                dividendModelAux.DividendYeld = Parser.ParseFloat("")
                dividendModelAux.MajorShareholder = ""
                dividendModelAux.NetProfit = Parser.ParseFloat(stock["profit"])
                dividendModelAux.Valuation = Parser.ParseFloat("")
                dividendModelAux.StockAvailableAmount = 0
                returnObj.append(dividendModelAux)
        return returnObj

def GetStocksJson(strEndPoint):
        # return open("C:\git\SoSI\\backend\stock\mock\dividendMock.json", "r") # Mock for tests
        return urllib.request.urlopen(strEndPoint) # Production

def Save(lstDividend):
        for dividend in lstDividend:
                if DividendDbCommand().Save(dividend) == False:
                        return False
        return True 

stocks = json.load(GetStocksJson(SERVICE_ENDPOINT))
filteredStocks = FilterStocks(stocks, STOCK_TYPE_TO_FILTER)
divdendObj = GetDividendModel(filteredStocks)

if Save(divdendObj) == False:
        raise SystemError()

print ("DONE!!!")