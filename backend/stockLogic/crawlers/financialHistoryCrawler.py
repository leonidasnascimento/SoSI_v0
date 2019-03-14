from models.financialDataModel import FinancialDataModel
from models.financialHistoryModel import FinancialHistoryModel
from helpers.web import Web
from helpers.parser import Parser
from datetime import date
import sys
import time
import threading
import re

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\var\\www\\git\\sosi\\backend")


# GLOBAL
URL_YAHOO_CASH_FLOW = "https://br.financas.yahoo.com/quote/%s.SA/cash-flow"
URL_YAHOO_BALANCE_SHEET = "https://br.financas.yahoo.com/quote/%s.SA/balance-sheet"

# FIELDS
FIELD_SHARED_DIVIDENDS = "Dividendos Pagos"
FIELD_NET_INCOME = "Lucro Líquido"
FIELD_NET_INCOME = "Lucro Líquido"
FIELD_NET_WORTH = "Patrimônio Líquido Total"

class FinancialHistoryCrawler(FinancialHistoryModel):

    def __init__(self, stockCode):
        self.Code = stockCode
        self.ListData = []
        self.DividendLabel = FIELD_SHARED_DIVIDENDS 
        self.NetIncomeLabel = FIELD_NET_INCOME
        self.NetWorthLabel = FIELD_NET_WORTH
        self.__setHistoryDate(FIELD_SHARED_DIVIDENDS, stockCode, URL_YAHOO_CASH_FLOW, True)
        self.__setHistoryDate(FIELD_NET_INCOME, stockCode, URL_YAHOO_CASH_FLOW, False)
        self.__setHistoryDate(FIELD_NET_WORTH, stockCode, URL_YAHOO_BALANCE_SHEET, False)
        pass

    def __setHistoryDate(self, rowToLookAt, stockCode, url, turnValueToPositive):
        urlAux = url % stockCode
        page = Web.GetWebPage(urlAux)

        if page is None:
            return

        periodList = []
        tdElement = None
        spanElement = None

        # gettin' the periods
        periodSection = page.find("span", text=re.compile('Final de Período'))

        if periodSection is None:
            return

        tdElement = periodSection.parent.find_next_sibling("td")
        while not (tdElement is None):
            spanElement = tdElement.find("span")

            if not (spanElement is None):
                dateAux = spanElement.get_text().split("/")

                if not (dateAux is None or dateAux == ""):
                    valDate = date(int(dateAux[2]), int(dateAux[1]), int(dateAux[0])).isoformat()
                    periodList.insert(len(periodList), valDate)

            tdElement = tdElement.find_next_sibling("td")

        # gettin' the values related to the period
        valueSection = page.find("span", text=re.compile(rowToLookAt))
        if valueSection is None:
            return

        tdElement = valueSection.parent.find_next_sibling("td")
        if tdElement is None:
            return

        for period in periodList:
            spanElement = tdElement.find("span")
            if spanElement is None:
                return

            valueAux = spanElement.get_text()
            valueFloat = 0.00

            if turnValueToPositive is True:
                valueFloat = (Parser.ParseFloat(valueAux) * -1)
            else:
                valueFloat = Parser.ParseFloat(valueAux)

            cashFlowObj = FinancialDataModel(rowToLookAt, period, (valueFloat * 1000))

            self.ListData.append(cashFlowObj)

            tdElement = tdElement.find_next_sibling("td")
            if tdElement is None:
                return
            pass
        pass
