import urllib
import json
import pprint
import sys
import requests
import urllib

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from crawlers.stockCrawler import StockCrawler
from crawlers.companyInfoCrawler import CompanyInfoCrawler
from bs4 import BeautifulSoup
from models.dividendModel import DividendModel
from helpers.parser import Parser
from database.dividendDbCommand import DividendDbCommand

### GLOBAL CONSTANTS ###
STOCK_TYPE_TO_FILTER = "ON"  # Leave it empty for all types

### GLOBAL VARIABLES ###
gStockTotalAmountObj = None
global_AvailableStocksSingleton = None

# FIELDS #
FIELD_RESULTS = "results"
FIELD_TYPE = "type"

# METHODS #
def GetDividendModel(stockObj):
    if stockObj is None: return
    
    returnObj = []
    for stock in stockObj.AvailableStockCode:
        dividendModelAux = DividendModel()
        companyInfo = CompanyInfoCrawler(stock["stockCode"])

        dividendModelAux.Code = stock["stockCode"]
        dividendModelAux.Company = stock["companyName"]
        dividendModelAux.Type = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockType")
        dividendModelAux.StockPrice = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockPrice")
        dividendModelAux.Sector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "primarySector")
        dividendModelAux.SecondSector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "secondarySector")
        dividendModelAux.Equity = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "equity")
        dividendModelAux.Avg21Negociation = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "avgNegociationValue")
        dividendModelAux.DividendLastPrice = GetDividendValue(stockObj.DividendsData, stock["stockCode"], 1)
        dividendModelAux.DividendPeriod = 0
        dividendModelAux.DividendYeld = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "dividendYeld")
        dividendModelAux.NetProfit = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "netProfit")
        dividendModelAux.StockAvailableAmount = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockAmount")
        dividendModelAux.AvgPayout12Months = (((dividendModelAux.DividendYeld * dividendModelAux.StockPrice) * dividendModelAux.StockAvailableAmount) / dividendModelAux.NetProfit)
        dividendModelAux.AvgPayout5Years = Parser.ParseFloat("")
        dividendModelAux.DividendTotalValueShared = dividendModelAux.AvgPayout12Months * dividendModelAux.NetProfit
        dividendModelAux.MajorShareholder = companyInfo.MajorShareholder
        dividendModelAux.Valuation = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "mktValue")
        
        companyInfo = None

        returnObj.append(dividendModelAux)
    return returnObj

def GetBasicInfo(lstToDigInto, stockCode, fieldToGet):
    if lstToDigInto is None: return ""
    
    lstReturn = []
    lstReturn = [ x[fieldToGet] for x in lstToDigInto if x["stock"] == stockCode ]

    if lstReturn is None or len(lstReturn) == 0: return ""

    return lstReturn[0] 

def GetDividendValue(lstToDigInto, stockCode, order: 1):
    if lstToDigInto is None: return ""
    
    lstDividend = []
    lstDividend = [ x["dividends"] for x in lstToDigInto if x["stockCode"] == stockCode ]
    dividendPrice = ""

    if lstDividend is None or len(lstDividend) == 0: return ""
    if lstDividend[0] is None or len(lstDividend[0]) == 0: return ""

    if order == 1: 
        dividendPrice = lstDividend[0][0]['dividend']
    else:
        dividendPrice = lstDividend[0][len(lstDividend[0]) - 1]['dividend']

    return dividendPrice

def Save(lstDividend):
    for dividend in lstDividend:
        if DividendDbCommand().Save(dividend) == False:
            return False
    return True

#########
## INI ##
#########

stockObj = StockCrawler(STOCK_TYPE_TO_FILTER)
lstDividend = GetDividendModel(stockObj)

if (lstDividend is None) or (Save(lstDividend)) == False:
    raise SystemError()

print("DONE!!!")
