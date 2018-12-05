from database.base.dbCommand import DbCommand
from stock.models.dividendModel import DividendModel

class DividendDb:
    def Save(self, obj):
        classObj = (DividendModel) (obj)
        str =   ("INSERT INTO DIVIDEND (ATIVO_SIGLA," + 
        "NOME_EMPRESA, SETOR_ATUACAO, SUBSETOR_ATUACAO, PRECO_ACAO," + 
        "TIPO_ACAO, EMPRESA_VAL_MERCADO, QTD_ACAO_OFERTADA, VOL_MEDIO_NEGOCIADO_21, " +
        "PER_PGTO_DIVIDENDOS, PRECO_DIVIDENDO_ACAO, QTD_DIVIDENDOS_PERIODO_VALOR, " +
        "LUCRO_LIQ_PERIODO_VALOR, DIVIDEND_YIELD, PAYOUT_MEDIO_DOZE_MESES, " + 
        "PAYOUT_MEDIO_CINCO_ANOS, NOME_MAIOR_ACIONISTA) VALUE (" + 
        classObj.Code, ", " + 
        classObj.Company, ", " +
        classObj.Sector, ", " +
        classObj.SecondSector, ", " +
        classObj.StockPrice, ", " +
        classObj.Type, ", " +
        classObj.Valuation, ", " +
        classObj.StockAvailableAmount, ", " +
        classObj.Avarage21Negociation, ", " +
        classObj.DividendPeriod, ", " +
        classObj.DividendLastPrice, ", " +
        classObj.DividendTotalValueShared, ", " +
        classObj.NetProfit, ", " +
        classObj.DividendYeld, ", " +
        classObj.AvgPayoutTwelveMonths, ", " +
        classObj.AvgPayoutFiveYears, ", " +
        classObj.MajorShareholder, ") ")
        return DbCommand().Save(str)