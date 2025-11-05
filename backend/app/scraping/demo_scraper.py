import random

from app.scraping.base import PriceQuote, PriceSource

class DemoScrapper(PriceSource):
    async def fetch(self, url: str) -> PriceQuote:
        price = random.randint(5000, 50000) #in cents and this is just for testing the pipeline
        return PriceQuote(url = url, price_cents = price, currency = "USD")