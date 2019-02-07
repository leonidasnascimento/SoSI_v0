from models.dividendDataModel import DividendDataModel

## GLOBAL
JCP_DESCRIPTION = "JCP"
DIVIDEND_DESCRIPTION = "DIVIDEND"

class DividendHistoryModel:
    StockCode: ""
    ListData: []

    def __init__(self, stock):
        self.ListData = []
        self.StockCode = stock

    def __addDividend(self, date, desc, value):
        self.ListData.append(DividendDataModel(date, desc, value))
        pass

    def AddDividend(self, date, value):
        self.__addDividend(date, DIVIDEND_DESCRIPTION, value)
    
    def AddJCP(self, date, value):
        self.__addDividend(date, JCP_DESCRIPTION, value)

    def GetItemByDescription(self, description):
        if self.ListData is None or len(self.ListData) == 0: return None
        
        resultList = [item for item in self.ListData if item.Description == description]

        return resultList

    def GetDividendLastValue(self):
        data = self.__getLastItemFromListByDescription(DIVIDEND_DESCRIPTION)
        if data is None: return 0.00
        
        return data.Value

    def GetDividendPeriod(self):
        return -1

    def GetJCPLastValue(self):
        data = self.__getLastItemFromListByDescription(JCP_DESCRIPTION)
        if data is None: return 0.00
        
        return data.Value

    def __getLastItemFromListByDescription(self, description):
        lst = self.GetItemByDescription(description)

        if lst is None or len(lst) == 0: return 0.00

        value = lst[len(lst) - 1]

        return value