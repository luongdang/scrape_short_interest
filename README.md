# Short Interest Scraping from Wall Street Journal

Scrape [short interest data][1] from the Wall Street Journal.

## Prerequisites

The Wall Street Journal implements a measure to guard against data scraping. The [short interest data][1] page does not contain any data. Instead it has Javascripts that trigger the loading of the actual data. Browsers such as Chrome or Safari can execute the Javascripts and thus display the results to end users. Web scrapers, however, cannot execute Javascripts and are left at the landing page.

To circumvent this restrictions, we need to run a browser in "headless" mode, i.e. having Chrome run in the background, load and execute the Javascripts, and then there will be actual data to scrape. We Selenium, an automated testing framework to help us do that.

```bash
# Install Selenium
pip install selenium
```

[1]: http://www.wsj.com/mdc/public/page/2_3062-shtnyse_A-listing.html
