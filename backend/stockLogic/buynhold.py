import pprint
import sys

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from database.buyNHoldDbCommand import BuyNHoldDbCommand
from helpers.parser import Parser
from models.buynHoldModel import BuyNHoldeModel
from crawlers.financialHistoryCrawler import FinancialHistoryCrawler
from crawlers.companyStatisticCrawler import CompanyStatisticCrawler
from crawlers.companyInfoCrawler import CompanyInfoCrawler
from crawlers.stockCrawler import StockCrawler

### GLOBAL CONSTANTS ###
STOCK_TYPE_TO_FILTER = ""  # Leave it empty for all types

### GLOBAL VARIABLES ###
gStockTotalAmountObj = None
global_AvailableStocksSingleton = None

# FIELDS #
FIELD_RESULTS = "results"
FIELD_TYPE = "type"

# METHODS #
def GetBuyNHoldModel(stockObj):
    if stockObj is None:
        return

    if stockObj.AvailableStockCode is None:
        return

    returnObj = []

    for stock in stockObj.AvailableStockCode:
        buyHoldModelAux = BuyNHoldeModel()
        companyInfo = CompanyInfoCrawler(stock["stockCode"])
        companyStatistic = CompanyStatisticCrawler(stock["stockCode"])
        financialHistData = FinancialHistoryCrawler(stock["stockCode"])

        buyHoldModelAux.Code = companyInfo.Code
        buyHoldModelAux.Company = companyInfo.Company
        buyHoldModelAux.Type = companyInfo.Type
        buyHoldModelAux.StockPrice = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockPrice", 0.00))
        buyHoldModelAux.Sector = companyInfo.Sector
        buyHoldModelAux.SecondSector = companyInfo.SecondSector
        buyHoldModelAux.Equity = financialHistData.GetLastNetWorth()
        buyHoldModelAux.Avg21Negociation = companyStatistic.AvgVolume3Months
        buyHoldModelAux.DividendLastPrice = float(GetDividendValue(stockObj.DividendsData, stock["stockCode"], 1, 0.00))
        buyHoldModelAux.DividendPeriod = 0
        buyHoldModelAux.DividendYeld = companyStatistic.DividendYeld
        buyHoldModelAux.NetProfit = financialHistData.GetLastNetIncome()
        buyHoldModelAux.StockAvailableAmount = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockAmount", 0))
        buyHoldModelAux.AvgPayout12Months = companyStatistic.PayoutRatio
        buyHoldModelAux.DividendTotalValueShared = companyStatistic.PayoutRatio * buyHoldModelAux.NetProfit
        buyHoldModelAux.MajorShareholder = companyInfo.MajorShareholder
        buyHoldModelAux.Valuation = companyStatistic.Valuation
        buyHoldModelAux.ReturnOnEquity = companyStatistic.ReturnOnEquity
        buyHoldModelAux.ReturnOnEquity_5yrAvg = companyStatistic.ReturnOnEquity_5yrAvg
        buyHoldModelAux.GrossDebitOverEbitda = companyStatistic.GrossDebitOverEbitida
        buyHoldModelAux.DividendYeld_5yrAvg = companyStatistic.DividendYeld_5yrAvg
        buyHoldModelAux.AvgPayout5Years = financialHistData.GetAvgDividendShared() / financialHistData.GetAvgNetIncome()
        buyHoldModelAux.HasDividendBeenSharedInLast5Yrs = financialHistData.HasDividendBeenSharedInLast5Yrs()
        buyHoldModelAux.HasDividendGrowthInLast5Yrs = financialHistData.HasDividendGrowthInLast5Yrs()
        buyHoldModelAux.HasNetProfitBeenRegularFor5Yrs = financialHistData.HasNetProfitBeenRegularFor5Yrs()

        print("%s - OK" % companyInfo.Code)

        companyInfo = None
        companyStatistic = None
        financialHistData = None

        returnObj.append(buyHoldModelAux)
    return returnObj


def GetBasicInfo(lstToDigInto, stockCode, fieldToGet, defaultValue):
    if lstToDigInto is None:
        return defaultValue

    lstReturn = []
    lstReturn = [x[fieldToGet]
                 for x in lstToDigInto if x["stock"] == stockCode]

    if lstReturn is None or len(lstReturn) == 0:
        return defaultValue

    return lstReturn[0] if str(lstReturn[0]) != "" or str(lstReturn[0]) != '' else defaultValue


def GetDividendValue(lstToDigInto, stockCode, order: 1, defaultValue):
    if lstToDigInto is None:
        return defaultValue

    lstDividend = []
    lstDividend = [x["dividends"]
                   for x in lstToDigInto if x["stockCode"] == stockCode]
    dividendPrice = defaultValue

    if lstDividend is None or len(lstDividend) == 0:
        return defaultValue
    if lstDividend[0] is None or len(lstDividend[0]) == 0:
        return defaultValue

    if order == 1:
        dividendPrice = lstDividend[0][0]['dividend']
    else:
        dividendPrice = lstDividend[0][len(lstDividend[0]) - 1]['dividend']

    return dividendPrice if dividendPrice != "" else defaultValue


def Save(lstDividend):
    for dividend in lstDividend:
        if BuyNHoldDbCommand().Save(dividend) == False:
            return False
    return True

#########
## INI ##
#########


stockObj = StockCrawler(STOCK_TYPE_TO_FILTER)
lstDividend = GetBuyNHoldModel(stockObj)

if (lstDividend is None) or (Save(lstDividend)) == False:
    raise SystemError()

print("DONE!!!")
