# Short Interest Scraping from Wall Street Journal

Scrape [short interest data][1] from the Wall Street Journal.

## Prerequisites

The Wall Street Journal implemented a measure to guard against data scraping. The [short interest data][1] page does not contain any data. Upon first load, it loads Javascripts that will in turn trigger the loading of the actual data. Browsers such as Chrome or Safari can execute the Javascripts and thus display the results to end users. Web scrapers, however, cannot execute Javascripts and are left at the landing page.

To circumvent this restrictions, we need to run a browser in "headless" mode, i.e. having Chrome run in the background, load and execute the Javascripts, and then there will be actual data to scrape. We will use Selenium, an automated testing framework to help us do that.

```bash
# Install Selenium
pip install selenium
```

## Usage

```python
python scrape.py
```

[1]: http://www.wsj.com/mdc/public/page/2_3062-shtnyse_A-listing.html
