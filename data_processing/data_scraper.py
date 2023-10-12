# Import necessary libraries
import ssl
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import time
import pandas as pd
import random
import numpy as np
import requests

# Define a function to scrape water quality data from a specific URL
def water_quality_scraper():
    text_data = ""
    url = 'https://dem.ri.gov/latest-bay-area-report'
    # Define headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # Bypass SSL verification
    ssl._create_default_https_context = ssl._create_unverified_context
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    prev = ""
    # Extract relevant text from the webpage
    for t in soup.findAll('article'):
        text = t.get_text(strip=True)
        if 'Bay Water Quality Report' in text:
            text_data = text

    # Split the text data based on specific patterns
    text_data = re.split(
        r'Weekly Water Quality Report|BART Weekly Report|DEM/DOH HAB phytoplankton monitoring report for', text_data)[1:]
    return (text_data)

# Define a function to clean the scraped water quality data
def clean_water_quality():
    data = water_quality_scraper()
    temp = []
    do = []
    chlor = []
    # Extract temperature, dissolved oxygen, and chlorophyll values
    for entry in data:
        temp.append(entry.split("°")[0][-5:])
        do.append(entry.split(" mg/L")[0][-1:])
        chlor.append(entry.split(" ug/L")[0][-4:])
        print(chlor)

# Define a function to scrape sample data from URI website
def URI_sample_scraper():
    URL = 'https://web.uri.edu/gso/research/plankton/data/'
    # Bypass SSL verification
    ssl._create_default_https_context = ssl._create_unverified_context
    FILETYPE = '.xls'

    soup = BeautifulSoup(urlopen(Request(URL)).read(), 'html.parser')
    xls_links = []
    # Extract links to Excel files from the webpage
    for link in soup.find_all('a'):
        if 'countdata' in link:
            file_link = link.get('href')
            xls_links.append(file_link)
            if FILETYPE in file_link:
                print(file_link)
                # Download and save the Excel file
                with open(link.text, 'wb') as file:
                    response = requests.get(file_link)
                    file.write(response.content)

    # Read the downloaded Excel file into a DataFrame
    xls = pd.ExcelFile('Phytoplankton Count Data (.xls)')
    df = pd.read_excel(xls, 'Count data')
    return df

# Main function to execute the scraping and cleaning functions
def main():
    clean_water_quality()
    URI_sample_scraper()

# Execute the main function if the script is run as the main module
if __name__ == "__main__":
    main()
