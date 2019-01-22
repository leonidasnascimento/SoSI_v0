import sys

sys.path.append("\\git\\SoSI\\backend")

from database.base.dbCommand import DbCommand
from stockLogic.models.buynHoldModel import BuyNHoldeModel

class BuyNHoldDbCommand:
    def Save(self, obj):
        if obj is None:
            raise Exception 


        args = (obj.Code, obj.Company, obj.Sector, obj.SecondSector, 
            obj.StockPrice, obj.Type, obj.Valuation, obj.StockAvailableAmount, obj.Avg21Negociation, 
            obj.DividendPeriod, obj.DividendLastPrice, obj.DividendTotalValueShared, 
            obj.NetProfit, obj.DividendYeld, obj.AvgPayout12Months, obj.AvgPayout5Years, obj.MajorShareholder,
            obj.ReturnOnEquity, obj.ReturnOnEquity_5yrAvg, obj.GrossDebitOverEbitda, 
            obj.DividendYeld_5yrAvg, obj.AvgPayout5Years, obj.HasDividendBeenSharedInLast5Yrs, 
            obj.HasDividendGrowthInLast5Yrs, obj.HasNetProfitBeenRegularFor5Yrs)
        
        strCmd = "CALL SP_INSERT_DIVIDEND ('%s', '%s', '%s', '%s', %.6f, '%s', %.6f, %d, %.6f, %d, %.6f, %.6f, %.6f, %.6f, %.6f, %.6f, '%s', %.6f, %.6f, %.6f, %.6f, %.6f, %d, %d, %d);" % args

        return DbCommand().Commit(strCmd)        
        # return DbCommand().CallProcedure("SP_INSERT_DIVIDEND", args)