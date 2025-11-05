from dataclasses import dataclass
from typing import Optional

@dataclass
class PriceQuote:
    url: str
    price_cents: Optional[int]
    currency: Optional[int]


class PriceSource:
    """Abstract scraper interface"""

    async def fetch(self, url: str) -> PriceQuote:
        raise NotImplementedError