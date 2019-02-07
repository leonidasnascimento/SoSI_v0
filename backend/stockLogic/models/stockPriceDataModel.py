from datetime import datetime

class StockPriceDataModel:
    High: 0.00
    Low: 0.00
    Openning: 0.00
    Closing: 0.00
    Adjusted: 0.00
    Volume: 0.00
    Date: datetime

    def __init__(self, high, low, openig, closing, adjusted, volume, date):
        self.High = high
        self.Low = low
        self.Openning = openig
        self.Volume = volume
        self.Closing = closing
        self.Adjusted = adjusted
        self.Date = date
    
