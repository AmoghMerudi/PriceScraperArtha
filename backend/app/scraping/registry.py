from app.scraping.demo_scraper import DemoScrapper
from app.scraping.amazon_scraper import AmazonScraper
from app.scraping.generic_scraper import GenericScraper

SCRAPER_REGISTRY = {
    "demo": DemoScrapper(),
    "amazon": AmazonScraper(),
    "generic": GenericScraper(),
}

def get_scraper(site: str):
    scraper = SCRAPER_REGISTRY.get(site)
    if not scraper:
        raise ValueError(f"No scraper found for site: {site}")
    return scraper