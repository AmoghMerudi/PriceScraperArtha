from app.scraping.demo_scraper import DemoScrapper

SCRAPER_REGISTRY = {
    "demo": DemoScrapper(),
    "amazon": DemoScrapper() #placeholder
}

def get_scraper(site: str):
    scraper = SCRAPER_REGISTRY.get(site)
    if not scraper:
        raise ValueError(f"No scraper found for site: {site}")
    return scraper