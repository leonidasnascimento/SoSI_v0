import sys
import requests
import time
import threading

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from bs4 import BeautifulSoup

class Web:
    @staticmethod
    def GetWebPage(url):
        success = False

        while(not success):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                htmlPage = requests.get(url, headers=headers)
                htmlData = htmlPage.content
                page = BeautifulSoup(htmlData, "html.parser")
                success = True
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
            finally:
                htmlPage.close()

        return page