from shortinterest import ShortInterest
import locale

locale.setlocale(locale.LC_ALL, "en_US")

results = ShortInterest.scrape(["AXP", "AA", "AGD", "BA"]) # American Express, Alcoa, Abeerdeen Global Dynamic, Boeing
for r in results:
    print(f"{r.symbol}: {r.currentShortInterest}")
