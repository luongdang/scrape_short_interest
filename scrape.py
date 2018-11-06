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
    # Selenium provides a different driver for each operating system
    osName = platform.system()
    if osName == "Darwin":
        driverPath = "./drivers/chromedriver_mac64"
    elif osName == "Windows":
        driverPath = "./drivers/chromedriver_win32"
    elif osName == "Linux":
        driverPath = "./drivers/chromedriver_linux64"
    else:
        raise Exception(f"No Chrome driver for operating system '{osName}'")

    # Get the list of default options for the Chrome driver. If you want to add
    # more options, use the `add_argument` function.
    options = webdriver.ChromeOptions()

    # Activate the `headless` option if you don't want Chrome to show up or if
    # you are doing it on the cloud.
    # options.add_argument("headless")

    driver = webdriver.Chrome(executable_path=driverPath, options=options)
    driver.implicitly_wait = 10
    return driver


def toFloat(series):
    """
    Convert a *column* of strings to float, returning NaN if the string cannot
    be converted.

    In Pandas, a column in a DataFrame is called a "series".

    The numbers from WSJ are presented in 3 ways:
    * Decimal digits only: '600'
    * Decimal digits with thousand separator: '12,000'
    * Placeholder for empty values: '---'
    
    The first type can be easiy converted to float. The second type must have
    its commas removed first. The third type will result in NaN (not a number).
    """
    return pd.to_numeric(series.str.replace(",", ""), errors="coerce")


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

            # `enumerate` allows us to get both the index and the item in the
            # list. For example:
            #   for index, item in enumerate(["a", "b", "c"]):
            #
            # will loop through:
            #   index = 0, item = "a"
            #   index = 1, item = "b"
            #   index = 2, item = "c"
            for index, row in enumerate(table.select("tr")):

                # Read up on "Python List Comprehension" for the line below
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

    # The default subscription syntax refer to the column header:
    #   df[2]           --> select the column whose header is the number 2
    #
    # To refer to the column at position 2 (the third column), use `iloc`:
    #   df.iloc[:, 2]   --> select the column at index 2
    #
    # The `:` means "all rows". All columns from the third one till the end are
    # numeric so we can use Python's slice syntax:
    #   df[:, 2:]       --> select all columns from index 2 till the end
    df.iloc[:, 2:] = df.iloc[:, 2:].apply(toFloat)

    return df


def export(filePath, dataFrame):
    writer = pd.ExcelWriter(filePath, engine="xlsxwriter")
    dataFrame.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.save()

# Eliminate one or both parameters to scrape for everything
data = scrape(exchanges=["nyse"], keys=["A", "0_9"])
export("ShortInterest.xlsx", data)
