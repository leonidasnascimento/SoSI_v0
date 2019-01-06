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
from models.companyStockStatistcModel import CompanyStockStatistcModel

## GLOBAL
URL = "https://br.financas.yahoo.com/quote/%s.SA/key-statistics"

class CompanyStockStatisticCrawler(CompanyStockStatistcModel):
    def __init__(self, stockCode):
        self.Code = stockCode
        self.__setAvgVolume(stockCode)

    def __setAvgVolume(self, stockCode):
        """
        
        Parameter
        ---------------
        stockCode: str
            Company's stock code.
                
        """
        
        avg3MonthsVolume = ""
        avg10DaysVolume = ""

        url = (URL % stockCode)
        page = Web.GetWebPage(url)

        if page is None: 
            self.AvgVolume3Months = 0.00
            self.AvgVolume10Days = 0.00
            return

        pgAvgVolume3Mos = page.find(text=re.compile('^Volume Médio \(3 meses\)'))
        pgAvgVolume10Days = page.find(text=re.compile('^Volume Médio \(10 dias\)'))

        if not (pgAvgVolume10Days is None):
            avg10DaysVolume = pgAvgVolume10Days.parent.parent.find_next_sibling("td").get_text()
        
        if not (pgAvgVolume3Mos is None):
            avg3MonthsVolume = pgAvgVolume3Mos.parent.parent.find_next_sibling("td").get_text()

        # filling the properties
        self.AvgVolume10Days = Parser.ParseOrdinalNumber(avg10DaysVolume)
        self.AvgVolume3Months = Parser.ParseOrdinalNumber(avg3MonthsVolume) 