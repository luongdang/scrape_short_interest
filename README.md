# Short Interest Scraping from Wall Street Journal

Scrape [short interest data][1] from the Wall Street Journal.

## Prerequisites

Make sure you have the following components installed:

1. [Anaconda][2]: a Python distribution that's geared toward data science. Download the latest version of Python 3.x. This script was develeloped and tested under Python 3.7
2. The [Chrome][3] browser.
3. [Visual Studio Code][4] (for your development machine only).

Before you start modifying the script, make sure you pull down the latest version from BitBucket. `cd` into the project folder on your computer and type:

```bash
git pull
```

## About the Wall Street Journal

The Wall Street Journal implements an anti-scraping guard for the [short interest data][1] page. Upon first load, it loads Javascripts that will trigger the loading of the actual data. Browsers such as Chrome or Safari can execute the Javascripts and display the results to end users. Web scrapers, however, cannot execute Javascripts and are left at the landing page with a bunch of Javascripts.

To circumvent this restriction, we need to drive a browser from Python, i.e. telling Chrome to load the page and execute the Javascripts, then scrape off the data that Chrome has loaded. We will use Selenium, an automated testing framework to help us do that.

```bash
# Install Selenium
conda install selenium
```

## Usage

```python
python scrape.py
```

[1]: http://www.wsj.com/mdc/public/page/2_3062-shtnyse_A-listing.html
[2]: https://www.anaconda.com/download/
[3]: https://www.google.com/chrome/
[4]: https://code.visualstudio.com/
