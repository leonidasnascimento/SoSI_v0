import urllib
import json
import pprint
import sys
import requests
import urllib

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from stock import Stock
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
def GetAvg21Negociation(stock_code):
    url = "https://www.infomoney.com.br/webservices/services.asmx/GetHistoryQuotesDataTable"

    querystring = {"hash": "cfcd208495d565ef66e7dff9f98764da"}

    payload = "{\"sEcho\":1,\"iDisplayStart\":0,\"iDisplayLength\":\"10\",\"iSortCol_0\":0,\"sSortDir_0\":\"desc\",\"sSearch\":\"\",\"Ativo\":\"%s\",\"Ativos\":null,\"DataIni\":null,\"DataFinish\":null,\"Desde\":null,\"Semana\":5,\"PeriodoIni\":null,\"Unidade\":null,\"ATV_DADO1\":\"1\",\"ATV_DADO2\":\"23\",\"ATV_DADO3\":\"2\",\"ATV_DADO4\":\"25\",\"ATV_DADO5\":\"3\",\"ATV_DADO6\":\"24\",\"ATV_DADO7\":\"10\",\"ATV_DADO8\":\"26\",\"ATV_DADO9\":\"9\",\"ATV_DADO10\":null,\"ATV_DADO11\":\"13\",\"ATV_DADO12\":null,\"ATV_DADO13\":\"8\",\"ATV_DADO14\":null,\"ATV_DADO15\":\"17\",\"ATV_DADO16\":null,\"ATV_DADO17\":\"14\",\"ATV_DADO18\":null,\"ATV_DADO19\":\"4\",\"ATV_DADO20\":null}" % stock_code
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://www.infomoney.com.br",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'content-type': "application/json; charset=UTF-8",
        'referer': "https://www.infomoney.com.br/mercados/ferramentas/historico-de-cotacoes/itub4",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        'cookie': "_gcl_au=1.1.1108519526.1544546369; _ga=GA1.3.1465434072.1544546369; _gid=GA1.3.803759816.1544546369; IMQuotesHistory=%7B%22Period%22%3A%220.5%22%2C%22Length%22%3A%2210%22%7D; nvg22862=997f535a4043233bc66d4229009|2_346; IM.Hash=cfcd208495d565ef66e7dff9f98764da; tt_c_vmt=1544546372; tt_c_c=search; tt_c_s=search; tt_c_m=search; tt.u=800A000A9F61015C425C4DB302924F96; __qca=P0-1928358265-1544546373645; __hstc=254361559.320355575949c5b130c0ac2a0cbb8fee.1544546374601.1544546374601.1544546374601.1; hubspotutk=320355575949c5b130c0ac2a0cbb8fee; __hssrc=1; tt.nprf=42; _ttdmp=E:1|A:1|X:1|LS:42; _dc_gtm_UA-2297695-11=1; _dc_gtm_UA-3531175-1=1; _gat_UA-2297695-22=1; _ttuu.s=1544546528130; InfoMoney.UserInfo=%7b%22UserId%22%3anull%2c%22UserAnonymusId%22%3a%22f7aea9ba-5617-444a-9af8-c2a438c73059%22%2c%22Profile%22%3a%22Visit%22%2c%22DateLastAccess%22%3a%222018-12-11T00%3a00%3a00-02%3a00%22%2c%22Navegg%22%3anull%2c%22Ip%22%3anull%2c%22Social%22%3anull%2c%22YearBirth%22%3anull%2c%22IsPartner%22%3afalse%2c%22Products%22%3anull%2c%22IsTailMatch%22%3afalse%2c%22TailHash%22%3anull%7d; __hssc=254361559.2.1544546374602",
        'cache-control': "no-cache",
        'postman-token': "c73bff72-5b2f-2838-aacc-f8610774f45c"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    histDataAux = response.json()['d']
    historicalData = json.loads(histDataAux) if histDataAux != '' else None

    if historicalData is None:
        return 0.00

    divCount = loopCount = int(historicalData['iTotalDisplayRecords']) if int(historicalData['iTotalDisplayRecords']) <= 21 else 21  
    result = 0.00
    
    for hist in historicalData['aaData']: 
        if loopCount == 0: 
                break
        result += Parser.ParseOrdinalNumber(hist[8])
        loopCount -= 1

    return result/divCount

def GetDividendModel(stockObj):
    if stockObj is None: return
    
    returnObj = []
    for stock in stockObj.AvailableStockCode:
        dividendModelAux = DividendModel()
        dividendModelAux.Code = stock["stockCode"]
        dividendModelAux.Company = stock["companyName"]
        dividendModelAux.Type = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockType")
        dividendModelAux.StockPrice = Parser.ParseFloat(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockPrice"))
        dividendModelAux.Sector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "primarySector")
        dividendModelAux.SecondSector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "secondarySector")
        dividendModelAux.Equity = Parser.ParseFloat("")
        dividendModelAux.Avg21Negociation = Parser.ParseFloat(GetBasicInfo(stockObj.stockCode, stock["stockCode"], "avgNegociationValue"))
        dividendModelAux.AvgPayout5Years = Parser.ParseFloat("")
        dividendModelAux.AvgPayout12Months = Parser.ParseFloat("")
        dividendModelAux.DividendLastPrice = Parser.ParseFloat(GetDividendValue(stockObj.DividendsData, stock["stockCode"], 1))
        dividendModelAux.DividendPeriod = 0
        dividendModelAux.DividendTotalValueShared = Parser.ParseFloat("")
        dividendModelAux.MajorShareholder = ""
        dividendModelAux.NetProfit = Parser.ParseFloat(GetBasicInfo(stockObj.stockCode, stock["stockCode"], "netProfit"))
        dividendModelAux.Valuation = Parser.ParseFloat(GetBasicInfo(stockObj.stockCode, stock["stockCode"], "mktValue"))
        dividendModelAux.StockAvailableAmount = Parser.ParseFloat(GetBasicInfo(stockObj.stockCode, stock["stockCode"], "stockAmount"))
        dividendModelAux.DividendYeld = dividendModelAux.DividendLastPrice / dividendModelAux.StockPrice
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
    lstDividend = [ x["dividends"] for x in lstToDigInto if x["stock"] == stockCode ]

    if lstDividend is None or len(lstDividend) == 0: return ""

    if order == 1: 
        return lstDividend.sort("date", True)[0]
    else:
        return lstDividend.sort("date")[0]

def Save(lstDividend):
    for dividend in lstDividend:
        if DividendDbCommand().Save(dividend) == False:
            return False
    return True

stockObj = Stock(STOCK_TYPE_TO_FILTER)
lstDividend = GetDividendModel(stockObj)

if (lstDividend is None) or (Save(lstDividend)) == False:
    raise SystemError()

print("DONE!!!")
