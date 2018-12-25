import sys
import time
import threading

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from dateutil import parser
from datetime import datetime
from helpers.parser import Parser
from helpers.web import Web
from models.companyInfoModel import CompanyInfoModel

## GLOBAL
URL = "https://br.advfn.com/bolsa-de-valores/bovespa/%s/empresa"

class CompanyInfoCrawler(CompanyInfoModel):

    def __init__(self, stockCode):
        self.__setMajorShareholder(stockCode)
    
    def __setMajorShareholder(self, stockCode):
        if stockCode == "" or stockCode == None: return None

        page = Web.GetWebPage(URL % stockCode)
        if page is None: 
            self.MajorShareholder = ""
            return

        div = page.find("div", {"class": "bx bx-stock-shares"})
        if div is None:
            self.MajorShareholder = ""
            return
        
        table = div.find('table', {"class": "table_element_class"})
        if table is None:
            self.MajorShareholder = ""
            return

        # Major Shareholder
        
        # <TABLE>
        if table.contents is None or len(table.contents) < 2: 
            self.MajorShareholder = ""
            return
        
        # <TR>
        if table.contents[1] is None or len(table.contents[1]) == 0:
            self.MajorShareholder = ""
            return

        # <TD>
        if table.contents[1].contents is None or len(table.contents[1].contents) == 0:
            self.MajorShareholder = ""
            return

        # POPULATIN THE OBJECT
        self.MajorShareholder = str(table.contents[1].contents[0].get_text()).lstrip().rstrip()