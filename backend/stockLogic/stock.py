import sys
import requests
import urllib
from bs4 import BeautifulSoup

## GLOBAL ##


class Stock:
    @staticmethod
    def GetAvailableStocksSingleton():
        __global_AvailableStocksSingleton = None

        if __global_AvailableStocksSingleton is not None:
            return __global_AvailableStocksSingleton

        htmlPage = urllib.request.urlopen(
            "http://www.fundamentus.com.br/detalhes.php")
        stocksPage = BeautifulSoup(htmlPage.read(), features="html.parser")

        if stocksPage is None:
            return __global_AvailableStocksSingleton

        stocksTbl = stocksPage.findChildren("table")

        if len(stocksTbl) == 0:
            return __global_AvailableStocksSingleton

        stocksRow = stocksTbl[0].findChildren("tr")

        if len(stocksRow) == 0:
            return __global_AvailableStocksSingleton

        for row in stocksRow:
            if row is None:
                continue

            columns = row.findChildren("td")

            if columns is None or len(columns) == 0:
                continue

            __global_AvailableStocksSingleton = __global_AvailableStocksSingleton if __global_AvailableStocksSingleton is not None else []
            det = columns[0].findChildren("a")

            stockAux = []

            if (det is not None) and len(det) > 0:
                stockAux.append(str(det[0].attrs["href"]).rstrip(None))
            else:
                continue
            
            stockAux.append(str(det.next()).rstrip(None))
            stockAux.append(columns[1].get_text())
            stockAux.append(columns[2].get_text())

            __global_AvailableStocksSingleton.append(stockAux)

        return __global_AvailableStocksSingleton

    @staticmethod
    def GetTagContent(contentArr):
        if (contentArr is None) or (len(contentArr.contents) == 0):
            return ""
        if (len(contentArr.contents) > 0) and (contentArr.contents[0].contents is None):
            return str(str(contentArr.contents[0]).lstrip(None)).rstrip(None)
        if (len(contentArr.contents[0].contents) == 0):
            return str(str(contentArr).lstrip(None)).rstrip(None)

        return Stock.GetTagContent(contentArr.contents[0])
