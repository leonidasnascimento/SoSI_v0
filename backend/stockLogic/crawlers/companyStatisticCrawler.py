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
from models.companyStatistcModel import CompanyStatistcModel

## GLOBAL
URL = "https://br.financas.yahoo.com/quote/%s.SA/key-statistics"
URL2 = "https://br.advfn.com/bolsa-de-valores/bovespa/%s/fundamentos"

class CompanyStatisticCrawler(CompanyStatistcModel):
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
        roe = ""
        grossDebitEbitda = ""
        payoutRatio = ""

        url = (URL % stockCode)
        page = Web.GetWebPage(url)

        if page is None: 
            self.AvgVolume3Months = 0.00
            self.AvgVolume10Days = 0.00
            self.ReturnOnEquity = 0.00
            self.GrossDebitOverEBITDA = 0.00
            self.PayoutRatio = 0.00
            return

        pgAvgVolume3Mos = page.find(text=re.compile('^Volume Médio \(3 meses\)'))
        pgAvgVolume10Days = page.find(text=re.compile('^Volume Médio \(10 dias\)'))
        pRoe = page.find(text=re.compile('^Retorno Sobre o Patrimônio Líquido'))
        pPayoutRatio = page.find(text=re.compile('^Índice de Payout'))        
        pGrossDebitEbitida = ""

        ###########
        ##  URL  ##
        ###########

        if not (pgAvgVolume10Days is None):
            avg10DaysVolume = pgAvgVolume10Days.parent.parent.find_next_sibling("td").get_text()
        
        if not (pgAvgVolume3Mos is None):
            avg3MonthsVolume = pgAvgVolume3Mos.parent.parent.find_next_sibling("td").get_text()

        if not (pRoe is None):
            roe = pRoe.parent.parent.find_next_sibling("td").get_text()

        if not (pPayoutRatio is None):
            payoutRation = pPayoutRatio.parent.parent.find_next_sibling("td").get_text()

        ###########
        ## URL 2 ##
        ###########

        url2 = (URL2 % stockCode)
        page2 = Web.GetWebPage(url2)

        if not (page2 is None):
            pGrossDebitEbitida = page2.find(text=re.compile('^Dívida Líquida \/ EBITDA'))

            if not (pGrossDebitEbitida is None):
                grossDebitEbitda = pGrossDebitEbitida.parent.find_next_sibling("td").get_text()

        # filling the properties
        self.AvgVolume10Days = Parser.ParseOrdinalNumber(avg10DaysVolume)
        self.AvgVolume3Months = Parser.ParseOrdinalNumber(avg3MonthsVolume)
        self.ReturnOnEquity = Parser.ParseFloat(roe)
        self.GrossDebitOverEBITDA = Parser.ParseFloat(grossDebitEbitda) / 100 
        self.PayoutRatio = Parser.ParseFloat(payoutRatio)