import sys

sys.path.append("\\git\\SoSI\\backend")

from database.base.dbCommand import DbCommand
from stockLogic.models.dividendModel import DividendModel

class DividendDbCommand:
    def Save(self, obj):
        if obj is None:
            raise Exception 


        args = (obj.Code, obj.Company, obj.Sector, obj.SecondSector, 
            obj.StockPrice, obj.Type, obj.Valuation, obj.StockAvailableAmount, obj.Avg21Negociation, 
            obj.DividendPeriod, obj.DividendLastPrice, obj.DividendTotalValueShared, 
            obj.NetProfit, obj.DividendYeld, obj.AvgPayout12Months, obj.AvgPayout5Years, obj.MajorShareholder)
        
        strCmd = "CALL SP_INSERT_DIVIDEND ('%s', '%s', '%s', '%s', %.2f, '%s', %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, '%s');" % args

        return DbCommand().Commit(strCmd)        
        # return DbCommand().CallProcedure("SP_INSERT_DIVIDEND", args)