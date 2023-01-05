# import statements
import ssl
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import time
import re
import pandas as pd
import random
import numpy as np
import re
import ssl
import requests


def water_quality_scraper():
    text_data = ""
    url = 'https://dem.ri.gov/latest-bay-area-report'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    ssl._create_default_https_context = ssl._create_unverified_context
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    prev = ""
    for t in soup.findAll('article'):
        text = t.get_text(strip=True)
        if 'Bay Water Quality Report' in text:
            text_data = text

    text_data = re.split(
        r'Weekly Water Quality Report|BART Weekly Report|DEM/DOH HAB phytoplankton monitoring report for', text_data)[1:]
    return (text_data)


def clean_water_quality():
    data = water_quality_scraper()
    temp = []
    do = []
    chlor = []
    for entry in data:
        temp.append(entry.split("°")[0][-5:])
        do.append(entry.split(" mg/L")[0][-1:])
        chlor.append(entry.split(" ug/L")[0][-4:])
        print(chlor)


def URI_sample_scraper():
    URL = 'https://web.uri.edu/gso/research/plankton/data/'
    ssl._create_default_https_context = ssl._create_unverified_context
    FILETYPE = '.xls'

    soup = BeautifulSoup(urlopen(Request(URL)).read(), 'html.parser')
    xls_links = []
    for link in soup.find_all('a'):
        if 'countdata' in link:
            file_link = link.get('href')
            xls_links.append(file_link)
            if FILETYPE in file_link:
                print(file_link)
                with open(link.text, 'wb') as file:
                    response = requests.get(file_link)
                    file.write(response.content)

    xls = pd.ExcelFile('Phytoplankton Count Data (.xls)')
    df = pd.read_excel(xls, 'Count data')
    return df


def WHOI_scraper():
    URL = 'https://habhub.whoi.edu'
    ssl._create_default_https_context = ssl._create_unverified_context
    req = requests.get(URL)
    soup = BeautifulSoup(req.text, 'html.parser')
    print(soup)
    # print(script)


def main():
    # clean_water_quality()
    # print(URI_sample_scraper())
    WHOI_scraper()


if __name__ == "__main__":
    main()
