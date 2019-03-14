from bs4 import BeautifulSoup
import ssl
import os
import requests
import sys

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\var\\www\\git\\sosi\\backend")

class Web:
    @staticmethod
    def GetWebPage(url):
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        htmlPage = requests.get(url, headers=headers, timeout=15)

        if htmlPage.status_code == 200:
            htmlData = htmlPage.content
            htmlPage.close()
            return BeautifulSoup(htmlData, "html.parser")
        else:
            return None
