from bs4 import BeautifulSoup
from datetime import datetime
from itertools import groupby
from selenium import webdriver
from selenium.webdriver.common.by import By

import locale
import platform
import string

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
        interest.currentShortInterest  = _tryConvert(locale.atoi, columns[2].text)
        interest.previousShortInterest = _tryConvert(locale.atoi, columns[3].text)
        interest.percentOfFloat        = _tryConvert(locale.atof, columns[6].text)
        interest.daysToCover           = _tryConvert(locale.atoi, columns[7].text)
        interest.averageDailyVolume    = _tryConvert(locale.atoi, columns[8].text)
        #
        interest.currentReportDate     = currentReportDate
        interest.previousReportDate    = previousReportDate

        return interest

    @classmethod
    def scrape(cls):
        # A `driver` allows us to drive Chrome from Python. To the WSJ, this is
        # indistinguiable from a user manually visiting the page.
        driver = _getChromeDriver()

        # The three exchanges available on the site
        exchanges = ["nyse", "nasdaq", "amex"]

        # A list containing the letters "a" to "z", plus the string "0-9"
        keys = list(string.ascii_uppercase) + ['0-9']

        # The result of the scrape
        results = []

        for exchange in exchanges:
            for key in keys:
                url = f"http://www.wsj.com/mdc/public/page/2_3062-sht{exchange}_{key}-listing.html"
                print(f"Scraping from {url}")

                # Open the page in Chrome. We are driving Chrome from Python
                driver.get(url)

                try:
                     # Never parse HTML using RegEx. Always use a proper parser
                     # like BeautifulSoup.
                    soup = BeautifulSoup(driver.find_element(By.TAG_NAME, "html").innerHTML)

                    # table.mdcTable is the CSS selector for "the <table> element
                    # with class mdcTable"
                    table = soup.select_one("table.mdcTable")

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
                    print(f"Skipping '{exchange}' and '{key}'")

        driver.quit()
        return results

def _tryConvert(convertFunc, str, defaultValue=None):
    try:
        return convertFunc(str)
    except ValueError:
        return defaultValue

def _getChromeDriver():
    osName = platform.system()
    if osName == "Darwin":
        driverPath = "drivers/chromedriver_mac64"
    elif osName == "Windows":
        driverPath = "drivers/chromedriver_win32"
    elif osName == "Linux":
        driverPath = "drivers/chromedriver_linux64"
    else:
        raise Exception(f"No Chrome driver for platform '{osName}'")

    options = webdriver.ChromeOptions()

    # Add the headless option if you don't want Chrome to show up or when you
    # are doing it on an Amazon EC2 instance
    # options.add_argument("headless")
    
    return webdriver.Chrome(executable_path=driverPath, options=options)
