from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

from itertools import groupby
import locale
import platform

class ShortInterest:
    def __init__(self):
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
        data = ShortInterest()
        data.name                  = columns[0].text
        data.symbol                = columns[1].text
        data.currentShortInterest  = _tryConvert(locale.atoi, columns[2].text)
        data.previousShortInterest = _tryConvert(locale.atoi, columns[3].text)
        data.percentOfFloat        = _tryConvert(locale.atof, columns[6].text)
        data.daysToCover           = _tryConvert(locale.atoi, columns[7].text)
        data.averageDailyVolume    = _tryConvert(locale.atoi, columns[8].text)
        #
        data.currentReportDate     = currentReportDate
        data.previousReportDate    = previousReportDate

        return data

    @classmethod
    def scrape(cls, symbols):
        symbolGroups = {}
        for key, symbols in groupby(symbols, lambda sym: sym[0].upper()):
            symbolGroups[key] = list(symbols)

        driver  = _getChromeDriver()
        results = []
        for key, symbols in symbolGroups.items():
            url = f"http://www.wsj.com/mdc/public/page/2_3062-shtnyse_{key}-listing.html"
            driver.get(url)
            
            table = driver.find_element(By.CSS_SELECTOR, "table.mdcTable")
            currentReportDate, previousReportDate = None, None
            for index, row in enumerate(table.find_elements(By.TAG_NAME, "tr")):
                columns = row.find_elements(By.TAG_NAME, "td")

                if index == 0:
                    formatString = "%m/%d/%y"
                    currentReportDate  = datetime.strptime(columns[2].text, formatString)
                    previousReportDate = datetime.strptime(columns[3].text, formatString)
                    continue
                
                symbol = columns[1].text
                if symbol in symbols:
                    interest = ShortInterest.__createFromColumns(columns, currentReportDate, previousReportDate)
                    results.append(interest)

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
    options.add_argument("headless")
    return webdriver.Chrome(executable_path=driverPath, options=options)
