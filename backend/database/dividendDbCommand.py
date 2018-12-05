import sys

sys.path.append("\\git\\SoSI\\backend")

from database.base.dbCommand import DbCommand
from stock.models.dividendModel import DividendModel

class DividendDbCommand:
    def Save(self, obj):
        str = ("INSERT INTO `sys`.`dividend` (`CODE`, `COMPANY`, `SECTOR`, `SECOND_SECTOR`," +
        "`STOCK_PRICE`, `STOCK_TYPE`, `VALUATION`, `STOCK_AVAILABLE_AMOUNT`, `AVG_21_NEGOCIATION`," +
        "`DIVIDEND_PERIOD`, `DIVIDEND_LAST_PRICE`, `DIVIDEND_TOTAL_VALUE_SHARED`, `NET_PROFIT`," +
        "`DIVIDEND_YELD`, `AVG_PAYOUT_12_MONTHS`, `AVG_PAYOUT_5_YEARS`, `MAJOR_SHARE_HOLDER`) VALUES" +
        "('%s','%s','%s','%s',%.2f,'%s',%.2f,%d,%d,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,'%s');" %
         (obj.Code, obj.Company, obj.Sector, obj.SecondSector, obj.StockPrice, 
         obj.Type, obj.Valuation, obj.StockAvailableAmount, obj.Avg21Negociation, 
         obj.DividendPeriod, obj.DividendLastPrice, obj.DividendTotalValueShared, 
         obj.NetProfit, obj.DividendYeld, obj.AvgPayout12Months, obj.AvgPayout5Years, obj.MajorShareholder)) 
        return DbCommand().Save(str)