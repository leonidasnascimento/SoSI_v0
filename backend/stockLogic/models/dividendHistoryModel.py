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

    def __addDividend(self, date, value, description):
        self.ListData.append(DividendDataModel(date, value, description))
        pass

    def AddDividend(self, date, value):
        self.__addDividend(date, value, DIVIDEND_DESCRIPTION)
    
    def AddJCP(self, date, value):
        self.__addDividend(date, value, JCP_DESCRIPTION)

    def GetItemByDescription(self, description):
        if self.ListData is None or len(self.ListData) == 0: return None
        
        resultList = [item for item in self.ListData if item.Description == description]

        return resultList
    
    def GetDividendLastValue(self):
        lst = self.GetItemByDescription(DIVIDEND_DESCRIPTION)

        if lst is None or len(lst) == 0: return 0.00

        value = lst[len(lst) - 1]

        return value
    
    def GetJCPLastValue(self):
        lst = self.GetItemByDescription(JCP_DESCRIPTION)

        if lst is None or len(lst) == 0: return 0.00

        value = lst[len(lst) - 1]

        return value