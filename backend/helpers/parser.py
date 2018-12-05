class Parser:
    @staticmethod
    def ParseFloat(valStr):
        if str(valStr).isspace() or valStr == "":
            return 0.00
        
        if valStr is None:
            return 0.00

        if str(valStr).find('.') > 0:
            valStr = str(valStr).replace('.', '')

        if str(valStr).find(',') > 0:
            valStr = str(valStr).replace(',', '.')
        
        return float(valStr)