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
        lpaAux = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "lpa", 0.00)

        dividendModelAux.Code = stock["stockCode"]
        dividendModelAux.Company = stock["companyName"]
        dividendModelAux.Type = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockType", "ND")
        dividendModelAux.StockPrice = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockPrice", 0.00))
        dividendModelAux.Sector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "primarySector", "")
        dividendModelAux.SecondSector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "secondarySector", "")
        dividendModelAux.Equity = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "equity", 0.00))
        dividendModelAux.Avg21Negociation = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "avgNegociationValue", 0.00))
        dividendModelAux.DividendLastPrice = float(GetDividendValue(stockObj.DividendsData, stock["stockCode"], 1, 0.00))
        dividendModelAux.DividendPeriod = 0
        dividendModelAux.DividendYeld = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "dividendYeld", 0.00))
        dividendModelAux.NetProfit = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "netProfit", 0.00))
        dividendModelAux.StockAvailableAmount = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockAmount", 0))

        # How To:
        #   https://pt.wikihow.com/Calcular-a-Taxa-de-Distribui%C3%A7%C3%A3o-de-Dividendos
        #
        if lpaAux > 0:
            dividendModelAux.AvgPayout12Months = (dividendModelAux.DividendYeld * dividendModelAux.StockPrice)/lpaAux 
        else:
            dividendModelAux.AvgPayout12Months = 0.00
        
        dividendModelAux.AvgPayout5Years = Parser.ParseFloat("")
        dividendModelAux.DividendTotalValueShared = dividendModelAux.AvgPayout12Months * dividendModelAux.NetProfit
        dividendModelAux.MajorShareholder = companyInfo.MajorShareholder
        dividendModelAux.Valuation = Parser.ParseFloat(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "mktValue", 0.00))
        
        companyInfo = None

        returnObj.append(dividendModelAux)
    return returnObj

def GetBasicInfo(lstToDigInto, stockCode, fieldToGet, defaultValue):
    if lstToDigInto is None: return defaultValue
    
    lstReturn = []
    lstReturn = [ x[fieldToGet] for x in lstToDigInto if x["stock"] == stockCode ]

    if lstReturn is None or len(lstReturn) == 0: return defaultValue

    return lstReturn[0] if str(lstReturn[0]) != "" or str(lstReturn[0]) != '' else defaultValue 

def GetDividendValue(lstToDigInto, stockCode, order: 1, defaultValue):
    if lstToDigInto is None: return defaultValue
    
    lstDividend = []
    lstDividend = [ x["dividends"] for x in lstToDigInto if x["stockCode"] == stockCode ]
    dividendPrice = defaultValue

    if lstDividend is None or len(lstDividend) == 0: return defaultValue
    if lstDividend[0] is None or len(lstDividend[0]) == 0: return defaultValue

    if order == 1: 
        dividendPrice = lstDividend[0][0]['dividend']
    else:
        dividendPrice = lstDividend[0][len(lstDividend[0]) - 1]['dividend']

    return dividendPrice if dividendPrice != "" else defaultValue

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
