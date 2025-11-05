import httpx
from selectolax.parser import HTMLParser

from app.scraping.base import PriceQuote, PriceSource

class AmazonScraper(PriceSource):
    async def fetch(self, url: str) -> PriceQuote:
        headers = {
            "User-Agent": (
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/118.0.0.0 Safari/537.36"
            ),
        }

        async with httpx.AsyncClient(timeout = 15.0) as client:
            response = await client.get(url, headers = headers)
            html = HTMLParser(response.text)

        selectors = [
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            "#corePriceDisplay_desktop_feature_div span.a-offscreen",
            "span.a-price-whole",
            "span.a-offscreen",
            "span.priceToPay span.a-offscreen"
        ]

        price_text = None
        for selector in selectors:
            node = html.css_first(selector)
            if node and node.text(strip = True):
                price_text = node.text(strip = True)
                if price_text:
                    print(f"[INFO] Found price '{price_text}' using selector '{selector}'")
                break
        
        if not price_text:
            print(f"[WARN] No price found for {url}")
            return PriceQuote(url=url, price_cents=None, currency="USD")

        try:
            cleaned = price_text.replace("$", "").replace(",", "").strip()
            price_cents = int(float(cleaned) * 100)
        except Exception as e:
            print(f"[ERROR] Failed to parse price for {url}: {e}")
            price_cents = None

        return PriceQuote(url=url, price_cents=price_cents, currency="USD")
