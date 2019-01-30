import sys
import time
import threading
import re

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from dateutil import parser
from datetime import datetime
from helpers.parser import Parser
from helpers.web import Web
from models.companyInfoModel import CompanyInfoModel

## GLOBAL
URL_MEUS_DIVIDENDOS = "https://www.meusdividendos.com/empresa/%s"
URL_YAHOO = "https://br.financas.yahoo.com/quote/%s.SA"

class CompanyInfoCrawler(CompanyInfoModel):

    def __init__(self, stockCode):
        self.Code = stockCode
        self.Company = ""
        self.MajorShareholder = ""
        self.SecondSector = ""
        self.Sector = ""
        self.Type = ""

        self.__setCompanyName(stockCode)
        self.__setMajorShareholder(stockCode)
    
    def __setCompanyName(self, stockCode):
        if stockCode == "" or stockCode == None: return
        
        self.Company = ""

        urlFormatted = URL_YAHOO % stockCode
        page = Web.GetWebPage(urlFormatted)
        if page is None: return

        h1 = page.find("h1", class_="D(ib) Fz(18px)")
        if h1 is None: return

        compAux1 = str(h1.get_text()).replace(("(%s.SA)" % stockCode), "")
        self.Company = str(compAux1).rstrip(' ')

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