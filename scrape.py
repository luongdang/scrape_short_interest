from bs4 import BeautifulSoup
from itertools import product
from locale import atof
from selenium import webdriver
from selenium.webdriver.common.by import By
from xlsxwriter import Workbook

import numpy as np
import pandas as pd
import platform
import string
import sys

def getChromeDriver():
    osName = platform.system()
    if osName == "Darwin":
        driverPath = "./drivers/chromedriver_mac64"
    elif osName == "Windows":
        driverPath = "./drivers/chromedriver_win32"
    elif osName == "Linux":
        driverPath = "./drivers/chromedriver_linux64"
    else:
        raise Exception(f"No Chrome driver for operating system '{osName}'")

    options = webdriver.ChromeOptions()

    # Activate the headless option if you don't want Chrome to show up or if
    # you are doing it on the cloud.
    # options.add_argument("headless")

    driver = webdriver.Chrome(executable_path=driverPath, options=options)
    driver.implicitly_wait = 10
    return driver


def toFloat(str, defaultValue=None):
    try:
        return float(str.replace(",", ""))
    except:
        return defaultValue


def scrape(exchanges=None, keys=None):
    # If user did not specify a list of exchanges, scrape all exchanges
    if exchanges is None:
        exchanges = ["nyse", "nasdaq", "amex"]
    
    # If use did not specify a list of keys, scrape all keys: all letters "A" to
    # "Z", plus the string "0_9"
    if keys is None:
        keys = list(string.ascii_uppercase) + ["0_9"]
    
    driver = getChromeDriver()
    headers = None
    data = []

    # The `product` function produces all possible combinations of the 2 lists:
    #   product(["A", "B"], [1, 2]) returns:
    #       [ ("A", 1), ("A", 2), ("B", 1), ("B", 2) ]
    #
    # Here, we are using it to replace nested loops. It's functionally
    # equivalent to:
    #   for exchange in exchanges:
    #       for key in keys:
    #
    for exchange, key in product(exchanges, keys):
        # Build the URL
        url = f"http://www.wsj.com/mdc/public/page/2_3062-sht{exchange}_{key}-listing.html"
        print(f"Scraping for '{exchange}', '{key}': {url}")
    
        # Tell Chrome to load the page
        driver.get(url)

        try:
            # Get the HTML markup for the table
            html = driver.find_element(By.CSS_SELECTOR, "table.mdcTable").get_attribute("innerHTML")

            # Never parse HTML using RegEx. Always use a proper parser like
            # BeautifulSoup.
            table = BeautifulSoup(html, "html.parser")

            for index, row in enumerate(table.select("tr")):
                # This is known as Python's list comprehension:
                #   results = [item.doSomething() for item in list]
                #
                # It's equivalent to:
                #   results = []
                #   for item in list:
                #       results.append(item.doSomething())
                #
                rowData = [col.get_text(" ", strip=True) for col in row.select("td")]

                if index == 0:
                    headers = rowData
                else:
                    data.append(rowData)
        except:
            print(f"Error parsing '{exchange}' and '{key}': {sys.exc_info()[1]}")

    # Close the browser
    driver.quit()

    # Construct the Pandas DataFrame
    df = pd.DataFrame(data=data, columns=headers)

    # Columns 2 - 8 contains numeric data. Convert them from string to float
    # range(2, 9) actually produces [2, 3, ..., 8]
    for col in range(2,9):
        df.iloc[:, col] = df.iloc[:, col].apply(toFloat)

    return df


def export(filePath, dataFrame):
    writer = pd.ExcelWriter(filePath, engine="xlsxwriter")
    dataFrame.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.save()


data = scrape(exchanges=["nyse"], keys=["A", "0_9"])
export("ShortInterest.xlsx", data)
