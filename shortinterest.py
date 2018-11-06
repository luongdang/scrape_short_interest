from bs4 import BeautifulSoup
from datetime import datetime
from itertools import groupby, product
from selenium import webdriver
from selenium.webdriver.common.by import By

import locale
import platform
import string
import sys

class ShortInterest:
    def __init__(self):
        # Python has no pre-declaration of properties. This initializer does
        # nothing but introduces instance properties of the `ShortInterest`
        # class so that the IDE can help us check for typos.
        self.name                  = None
        self.symbol                = None
        self.currentShortInterest  = None
        self.currentReportDate     = None
        self.previousShortInterest = None
        self.previousReportDate    = None
        self.percentOfFloat        = None
        self.daysToCover           = None
        self.averageDailyVolume    = None

    @classmethod
    def __createFromColumns(cls, columns, currentReportDate, previousReportDate):
        """
         Create a `ShortInterest` object from the contents of the specified columns.
         """

        interest = ShortInterest()
        interest.name                  = columns[0].text
        interest.symbol                = columns[1].text
        interest.currentShortInterest  = _toFloat(columns[2].text)
        interest.previousShortInterest = _toFloat(columns[3].text)
        interest.percentOfFloat        = _toFloat(columns[6].text)
        interest.daysToCover           = _toFloat(columns[7].text)
        interest.averageDailyVolume    = _toFloat(columns[8].text)
        #
        interest.currentReportDate     = currentReportDate
        interest.previousReportDate    = previousReportDate

        return interest

    @classmethod
    def scrape(cls, exchanges=["nyse", "nasdaq", "amex"], keys=None):
        # A `driver` allows us to drive Chrome from Python. To the WSJ, this
        # is indistinguiable from a user manually visiting the page.
        driver = _getChromeDriver()

        # If the user does not provide a list of key, use the default list,
        # which contains the letters "a" to "z", plus the string "0-9"
        if keys is None:
            keys = list(string.ascii_uppercase) + ['0_9']
        else:
            keys = map(keys, lambda k: k.upper())

        # A variable to hold the result of the scrape
        results = []

        # The `product` function produces all possible combinations between the
        # elements in the two arrays. We use it as a replacement for nested
        # loop. It is functionally equivalent to:
        #   for exchange in exchanges:
        #       for key in keys:
        #           ...
        for exchange, key in product(exchanges, keys):
            url = f"http://www.wsj.com/mdc/public/page/2_3062-sht{exchange}_{key}-listing.html"
            print(f"Scraping for '{exchange}', '{key}': {url}")

            # Open the page in Chrome. We are driving Chrome from Python
            driver.get(url)

            try:
                # Never parse HTML using RegEx. Always use a proper parser like
                # BeautifulSoup.
                html = driver.find_element(By.CSS_SELECTOR, "table.mdcTable").get_attribute("innerHTML")
                table = BeautifulSoup(html, "html.parser")

                # table.mdcTable is the CSS selector for "the <table> element
                # with class mdcTable"
                # table = soup.select_one("table.mdcTable")

                # This is Python tuple-spread syntax:
                #     x, y = 1, 2
                # means the same thing as:
                #     x = 1
                #     y = 2
                currentReportDate, previousReportDate = None, None
                count = 0

                # `enumerate` allows us to get both the index and the element
                # of an array. For example:
                #       for index, char in ["A", "B", "C"]:
                #
                # Will iterate through (index=0, char="A"), (index=1, char="B"),
                # (index=2, char = "C")
                for index, row in enumerate(table.select("tr")):
                    columns = row.select("td")

                    if index == 0:
                        formatString = "%m/%d/%y"
                        currentReportDate  = datetime.strptime(columns[2].text, formatString)
                        previousReportDate = datetime.strptime(columns[3].text, formatString)
                    else:
                        count += 1
                        results.append(ShortInterest.__createFromColumns(columns, currentReportDate, previousReportDate))

                print(f"Scraped {count} symbols")
            except:
                print(f"Error parsing '{exchange}' and '{key}': {sys.exc_info()[1]}")

        driver.quit()
        return results


def _toFloat(str, defaultValue=None):
    try:
        return float(str.replace(",", ""))
    except:
        return defaultValue


def _getChromeDriver():
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
    # you are doing it on an Amazon EC2 instance.
    # options.add_argument("headless")
    
    driver = webdriver.Chrome(executable_path=driverPath, options=options)
    driver.implicitly_wait = 10
    return driver
