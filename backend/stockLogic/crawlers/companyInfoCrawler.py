import sys
import time
import threading
import re

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\var\\www\\git\\sosi\\backend")

from dateutil import parser
from datetime import datetime
from helpers.parser import Parser
from helpers.web import Web
from models.companyInfoModel import CompanyInfoModel

## GLOBAL
URL_MEUS_DIVIDENDOS = "https://www.meusdividendos.com/empresa/%s"
URL_YAHOO = "https://br.financas.yahoo.com/quote/%s.SA/profile"

class CompanyInfoCrawler(CompanyInfoModel):

    stockTypeSwitcher = {
        1: "ON",
        2: "PN",
        3: "ON",
        4: "PN",
        5: "PN",
        6: "PN",
        7: "PN",
        8: "PN",
        9: "ON"
    }

    def __init__(self, stockCode):
        self.Code = stockCode
        self.Company = ""
        self.MajorShareholder = ""
        self.SecondSector = ""
        self.Sector = ""
        self.Type = ""
        self.StockLastPrice = 0.00
        self.StockAmountAvailable = 0.00

        self.__setCompanyNameSectorSubsector(stockCode)
        self.__setMajorShareholder(stockCode)
        self.__setStockType(stockCode)
        self.__setStockLastPrice(stockCode)
        self.__setStockAmountAvailable(stockCode)

    def __setStockAmountAvailable(self, stockCode):
        if stockCode == "" or stockCode == None: return
        
        self.StockAmountAvailable = 0.00

        lstWords = list(stockCode)
        urlFormatted = URL_MEUS_DIVIDENDOS % str(stockCode).replace(lstWords[len(lstWords)-1], '')
        
        page = Web.GetWebPage(urlFormatted)
        if page is None: return

        spanStocks = page.find("span", text=re.compile('Ações em Circulação'))
        if spanStocks is None: return
        
        spanStocksValue = spanStocks.find_next_sibling("span")
        if spanStocksValue is None: return

        value = spanStocksValue.get_text()
        self.StockAmountAvailable = float(value)

        pass

    def __setStockLastPrice(self, stockCode):
        if stockCode == "" or stockCode == None: return
        
        urlFormatted = URL_YAHOO % stockCode
        page = Web.GetWebPage(urlFormatted)
        if page is None: return

        spanLastPrice = page.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
        if spanLastPrice is None: return

        value = spanLastPrice.get_text()
        self.StockLastPrice = value

        pass

    def __setStockType(self, stockCode):
        if stockCode == "" or stockCode == None: return
        
        lstWords = list(stockCode)

        if lstWords is None: return
        if len(lstWords) == 0: return

        stockNumber = lstWords[len(lstWords) - 1]
        typeAux = ""

        if(str(stockNumber).isnumeric()): 
            typeAux = self.stockTypeSwitcher.get(int(stockNumber), "ND")

        self.Type = typeAux 
        pass

    def __setCompanyNameSectorSubsector(self, stockCode):
        if stockCode == "" or stockCode == None: return
        
        self.Company = ""
        self.Sector = ""
        self.SecondSector = ""

        urlFormatted = URL_YAHOO % stockCode
        page = Web.GetWebPage(urlFormatted)
        if page is None: return

        h1 = page.find("h1", class_="D(ib) Fz(18px)")
        if h1 is None: return

        compAux1 = str(h1.get_text()).replace(("(%s.SA)" % stockCode), "")
        self.Company = str(compAux1).rstrip(' ')

        spanSector = page.find("span", text=re.compile('Setor'))
        if spanSector is None: return
        
        spanSectorValue = spanSector.find_next_sibling("span")
        if spanSectorValue is None: return

        self.Sector = spanSectorValue.get_text()

        spanSecondSector = page.find("span", text=re.compile('Indústria'))
        if spanSecondSector is None: return
        
        spanSecondSectorValue = spanSecondSector.find_next_sibling("span")
        if spanSecondSectorValue is None: return

        self.SecondSector = spanSecondSectorValue.get_text()

        pass

    def __setMajorShareholder(self, stockCode):
        if stockCode == "" or stockCode == None: return
        
        self.MajorShareholder = ""

        lstWords = list(stockCode)
        urlFormatted = URL_MEUS_DIVIDENDOS % str(stockCode).replace(lstWords[len(lstWords)-1], '')
        
        page = Web.GetWebPage(urlFormatted)
        if page is None: return

        span = page.find("span", text=re.compile(' Principais Acionistas'))
        if span is None: return

        table = span.parent.parent.find_next_sibling("div").find("table")
        if table is None: return

        tbody = table.next()[0].parent.next_sibling
        if tbody is None: return

        majorShareholderAux = tbody.find("td").get_text()
        self.MajorShareholder = majorShareholderAux

        pass        