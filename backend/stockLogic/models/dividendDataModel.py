import datetime

class DividendDataModel:
    Date: datetime.datetime
    Description: ""
    Value: 0.00

    def __init__(self, date, desc, value):
        self.Description = desc
        self.Value = value
        self.Date = date