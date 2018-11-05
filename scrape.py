from shortinterest import ShortInterest
import locale

locale.setlocale(locale.LC_ALL, "en_US")

results = ShortInterest.scrape()
for r in results:
    print(f"{r.symbol}: {r.currentShortInterest}")
