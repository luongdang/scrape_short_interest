from shortinterest import ShortInterest
from xlsxwriter import Workbook

results = ShortInterest.scrape(exchanges=["nyse"], keys=["A"])
book = Workbook("ShortInterest.xlsx")
sheet = book.add_worksheet()

headers = [
    "Company Name",
    "Symbol",
    "Current Short Interest",
    "Previous Short Interest"
]
for col, h in enumerate(headers):
    sheet.write(0, col, h)

for row, r in enumerate(results):
    sheet.write(row + 1, 0, r.name )
    sheet.write(row + 1, 1, r.symbol)
    sheet.write(row + 1, 2, r.currentShortInterest)
    sheet.write(row + 1, 3, r.previousShortInterest)

book.close()