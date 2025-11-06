import httpx

from app.scraping.base import PriceQuote, PriceSource
from app.llm.client import extract_price_from_html
from app.scraping.render import get_rendered_html

class GenericScraper(PriceSource):
    async def fetch(Self, url: str) -> PriceQuote:
        try:
            html = await get_rendered_html(url)
        except Exception as e:
            print(f"[ERROR] Failed to render {url}: {e}")
            return PriceQuote(url=url, price_cents=None, currency=None)

        print(f"[DEBUG] HTML length for {url}: {len(html)}")
        print(len(html))

        data = await extract_price_from_html(html)
        print(f"[INFO] Parsed data from Llama for {url}: {data}")
        if not data:
            print(f"[WARN] Llama failed to extract price from {url}")
            return PriceQuote(url=url, price_cents=None, currency=None)
        
        price_cents = int(float(data["price"]) * 100)
        
        return PriceQuote(
            url = url, 
            price_cents = price_cents,
            currency = data.get("currency", "USD"),
        )