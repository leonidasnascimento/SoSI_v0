from models.cashFlowDataModel import CashFlowDataModel

class CashFlowHistoryModel:
    Code: ""
    ListData: []
    DividendLabel: ""
    NetIncomeLabel: ""

    def GetFromListDataByDescription(self, description):
        return []

    def GetFromListDataByDate(self, date):
        return []

    def GetFromListDataByDescriptionAndDate(self, description, date):
        return []

    def GetAvgNetIncome(self):
        netIncomeValueList = [data.Value for data in self.ListData if data.Description == self.NetIncomeLabel]
        netIncomeAvg = sum(netIncomeValueList) / len(netIncomeValueList if len(netIncomeValueList) > 0 else 1)
        
        return netIncomeAvg
    
    def GetAvgDividendShared(self):
        dividendValueList = [data.Value for data in self.ListData if data.Description == self.DividendLabel]
        dividendAvg = sum(dividendValueList) / len(dividendValueList if len(dividendValueList) > 0 else 1)

        return dividendAvg