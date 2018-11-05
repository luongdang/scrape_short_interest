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
        # A `driver` allows us to drive Chrome from Python. To the WSJ, this is
        # indistinguiable from a user manually visiting the page.
        driver = _getChromeDriver()

        # A list containing the letters "a" to "z", plus the string "0-9"
        if keys is None:
            keys = list(string.ascii_uppercase) + ['0_9']

        # The result of the scrape
        results = []
        for exchange, key in product(exchanges, keys):
            url = f"http://www.wsj.com/mdc/public/page/2_3062-sht{exchange}_{key}-listing.html"
            print(f"Scraping from {url}")

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

    # Add the headless option if you don't want Chrome to show up or when you
    # are doing it on an Amazon EC2 instance
    # options.add_argument("headless")
    
    return webdriver.Chrome(executable_path=driverPath, options=options)
