class DividendModel:
    Code: ""
    Company: ""
    Sector: ""
    SecondSector: ""
    StockPrice: 0.00
    Type: ""
    StockAvailableAmount: 0
    Valuation: 0.00
    Equity: 0.00
    Avg21Negociation: 0
    DividendPeriod: 0
    DividendLastPrice: 0.00
    DividendTotalValueShared: 0.00
    NetProfit: 0.00
    DividendYeld: 0.00
    AvgPayout12Months: 0.00
    AvgPayout5Years: 0.00
    MajorShareholder: ""

    def setAvaragePayout(self, payoutArray, netProfitArray):
        return (sum(payoutArray, 0)/ (sum(payoutArray, 0) if netProfitArray != 0 else 1))
    
    def setAvaragePayoutTwelveMonth(self, payoutArray, netProfitArray):
        self.AvgPayoutTwelveMonths = self.setAvaragePayout(payoutArray, netProfitArray)

    def setAvaragePayoutFiveYeats(self, payoutArray, netProfitArray):
        self.AvgPayoutFiveYears = self.setAvaragePayout(payoutArray, netProfitArray)

    def setValuation(self):
        self.Valuation = (self.StockPrice * self.StockAvailableAmount)
    
    def setDividendYield(self):
        self.DividendYeld = self.DividendLastPrice/(self.StockPrice if (self.StockPrice != 0) else 1)
    
