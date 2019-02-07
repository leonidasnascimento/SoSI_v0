from models.stockPriceDataModel import StockPriceDataModel

class StockPriceHistoryModel(StockPriceDataModel):
    ListData: []
    StockCode: ""

    def __init__(self, stockCode):
        self.ListData = []
        self.StockCode = stockCode

    def AddStockPrice(self, high, low, openig, closing, adjusted, volume, date):
        if self.ListData is None: self.ListData = []
        
        self.ListData.append(StockPriceDataModel(high, low, openig, closing, adjusted, volume, date))
    
    def GetAvgVolume(self):
        if self.ListData is None: return 0.00
        if len(self.ListData) == 0: return 0.00
        
        volumes = [data.Volume for data in self.ListData]
        avg = sum(volumes) / len(volumes) if len(volumes) > 0 else 1

        return avg

    def GetLastStockPrice(self):
        if self.ListData is None: return 0.00
        if len(self.ListData) == 0: return 0.00

        lastValue = self.ListData[0]

        return lastValue.Adjusted

        