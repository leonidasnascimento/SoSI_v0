import datetime

from models.financialDataModel import FinancialDataModel

class FinancialHistoryModel:
    Code: ""
    ListData: []
    DividendLabel: ""
    NetIncomeLabel: ""
    NetWorthLabel: ""

    def GetAvgNetIncome(self):
        if self.ListData is None: return 0  
        
        netIncomeValueList = [data.Value for data in self.ListData if data.Description == self.NetIncomeLabel]
        netIncomeAvg = sum(netIncomeValueList) / len(netIncomeValueList) if len(netIncomeValueList) > 0 else 1
        
        return netIncomeAvg
    
    def GetLastNetIncome(self):
        value = self.__GetLastValueFromHistory(self.NetIncomeLabel)
        return value

    def GetLastNetWorth(self):
        value = self.__GetLastValueFromHistory(self.NetWorthLabel)
        return value
    
    def __GetLastValueFromHistory(self, label):
        if self.ListData is None: return 0  
        
        valueList = [data.Value for data in self.ListData if data.Description == label]
        if valueList is None: return 0.00
        if len(valueList) == 0: return 0.00

        value = valueList[0]        
        return value

    def GetAvgDividendShared(self):
        if self.ListData is None: return 0  

        dividendValueList = [data.Value for data in self.ListData if data.Description == self.DividendLabel]
        dividendAvg = sum(dividendValueList) / len(dividendValueList) if len(dividendValueList) > 0 else 1

        return dividendAvg
    
    def HasDividendBeenSharedInLast5Yrs(self):
        if self.ListData is None: return 0    

        dividendValueList = [data.Value for data in self.ListData if data.Description == self.DividendLabel]
        dividendZeroValueList = [data for data in dividendValueList if data == 0]

        if len(dividendZeroValueList) == 0:
            return 1
        else:
            return 0

    def HasDividendGrowthInLast5Yrs(self):
        lstAux = [data for data in self.ListData if data.Description == self.DividendLabel]
        nextVal = self.GetSimpleLinearRegression(lstAux, datetime.date.today().year)
        
        if len(lstAux) == 0:
            return 0

        if (nextVal > lstAux[0].Value):
            return 1
        else:
            return 0
    
    def HasNetProfitBeenRegularFor5Yrs(self):
        lstAux = [data for data in self.ListData if data.Description == self.NetIncomeLabel]
        nextVal = self.GetSimpleLinearRegression(lstAux, datetime.date.today().year)
        
        if len(lstAux) == 0:
            return 0

        if (nextVal > lstAux[len(lstAux)-1].Value):
            return 1
        else:
            return 0
    
    def GetSimpleLinearRegression(self, list, nextXValue):
        returnValue = 0.00
        tg = 0.00

        if list is None: return returnValue
        
        x1 = datetime.datetime.strptime(list[0].Date, "%Y-%m-%d").year if (len(list) >= 1) else 0 
        x2 = datetime.datetime.strptime(list[1].Date, "%Y-%m-%d").year if (len(list) > 1) else 0 
        y1 = list[0].Value if (len(list) >= 1) else 0
        y2 = list[1].Value if (len(list) > 1) else 0
        tg = (y2 - y1)/((x2 - x1) if ((x2 - x1) != 0) else 1)
        b = y1 - (tg * x1)
        returnValue = (tg * nextXValue) + b

        return returnValue
        