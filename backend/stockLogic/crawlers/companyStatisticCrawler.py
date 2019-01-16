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
URL_ADVFN_FUNDAMENTOS = "https://br.advfn.com/bolsa-de-valores/bovespa/%s/fundamentos"
URL_REUTERS_FINANCIAL_HIGHLIGHTS = "https://www.reuters.com/finance/stocks/financial-highlights/%s.SA"

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
        roe_avg5yrs = ""

        url = (URL % stockCode)
        page = Web.GetWebPage(url)

        if page is None: 
            self.AvgVolume3Months = 0.00
            self.AvgVolume10Days = 0.00
            self.ReturnOnEquity = 0.00
            self.GrossDebitOverEbitida = 0.00
            self.PayoutRatio = 0.00
            self.GrossDebitOverEbitida_5yrAvg = 0.00
            return

        pgAvgVolume3Mos = page.find(text=re.compile('^Volume Médio \(3 meses\)'))
        pgAvgVolume10Days = page.find(text=re.compile('^Volume Médio \(10 dias\)'))
        pRoe = page.find(text=re.compile('^Retorno Sobre o Patrimônio Líquido'))
        pPayoutRatio = page.find(text=re.compile('^Índice de Payout'))        
        pGrossDebitEbitida = ""
        pRoe_avg5yrs = ""

        #############
        ##  YAHOO  ##
        #############

        if not (pgAvgVolume10Days is None):
            avg10DaysVolume = pgAvgVolume10Days.parent.parent.find_next_sibling("td").get_text()
        
        if not (pgAvgVolume3Mos is None):
            avg3MonthsVolume = pgAvgVolume3Mos.parent.parent.find_next_sibling("td").get_text()

        if not (pRoe is None):
            roe = pRoe.parent.parent.find_next_sibling("td").get_text()

        if not (pPayoutRatio is None):
            payoutRation = pPayoutRatio.parent.parent.find_next_sibling("td").get_text()

        ###########
        ## ADVFN ##
        ###########

        url_advfn_aux = (URL_ADVFN_FUNDAMENTOS % stockCode)
        page_advfn = Web.GetWebPage(url_advfn_aux)

        if not (page_advfn is None):
            pGrossDebitEbitida = page_advfn.find(text=re.compile('^Dívida Líquida \/ EBITDA'))

            if not (pGrossDebitEbitida is None):
                grossDebitEbitda = pGrossDebitEbitida.parent.find_next_sibling("td").get_text()

        #############
        ## REUTERS ##
        #############

        url_reuters_financial = (URL_REUTERS_FINANCIAL_HIGHLIGHTS % stockCode)
        page_reuters_financial = Web.GetWebPage(url_reuters_financial)

        if not (page_reuters_financial is None):
            pRoe_avg5yrs = page_reuters_financial.find(text=re.compile('Return on Equity - 5 Yr\. Avg\.'))
            
            if not (pRoe_avg5yrs is None):
                roe_avg5yrs = pRoe_avg5yrs.parent.find_next_sibling("td").get_text()

        # filling the properties
        self.AvgVolume10Days = Parser.ParseOrdinalNumber(avg10DaysVolume)
        self.AvgVolume3Months = Parser.ParseOrdinalNumber(avg3MonthsVolume)
        self.ReturnOnEquity = Parser.ParseFloat(roe)
        self.GrossDebitOverEbitida = Parser.ParseFloat(grossDebitEbitda) / 100 
        self.PayoutRatio = Parser.ParseFloat(payoutRatio)
        self.GrossDebitOverEbitida_5yrAvg = float(roe_avg5yrs) / 100