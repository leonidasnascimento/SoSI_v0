import DateTime

class FinancialDataModel:
    Description: ""
    Date: ""
    Value: 0.00

    def __init__(self, description, date, value):
        self.Description = description
        self.Value = value
        self.Date = date