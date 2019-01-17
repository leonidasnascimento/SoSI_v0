from models.cashFlowDataModel import CashFlowDataModel
from models.cashFlowHistoryModel import CashFlowHistoryModel
from helpers.web import Web
from helpers.parser import Parser
from datetime import date
import sys
import time
import threading
import re

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")


# GLOBAL
URL_YAHOO_CASH_FLOW = "https://br.financas.yahoo.com/quote/%s.SA/cash-flow"

# FIELDS
FIELD_SHARED_DIVIDENDS = "Dividendos Pagos"
FIELD_NET_INCOME = "Lucro Líquido"


class CashFlowHistoryCrawler(CashFlowHistoryModel):

    def __init__(self, stockCode):
        self.Code = stockCode
        self.ListData = []
        self.DividendLabel = FIELD_SHARED_DIVIDENDS 
        self.NetIncomeLabel = FIELD_NET_INCOME
        self.__setHistoryDate(FIELD_SHARED_DIVIDENDS, stockCode, True)
        self.__setHistoryDate(FIELD_NET_INCOME, stockCode, False)
        pass

    def __setHistoryDate(self, cashFlowRowToLookAt, stockCode, turnValueToPositive):
        url = URL_YAHOO_CASH_FLOW % stockCode
        page = Web.GetWebPage(url)

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
        valueSection = page.find("span", text=re.compile(cashFlowRowToLookAt))
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

            cashFlowObj = CashFlowDataModel(cashFlowRowToLookAt, period, valueFloat)

            self.ListData.append(cashFlowObj)

            tdElement = tdElement.find_next_sibling("td")
            if tdElement is None:
                return
            pass
        pass
