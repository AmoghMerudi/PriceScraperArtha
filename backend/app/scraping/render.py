from playwright.async_api import async_playwright
import asyncio

async def get_rendered_html(url: str) -> str:
    """Fetch fully rendered HTML from a page using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await asyncio.sleep(10)
            html = await page.content()
            print("[DEBUG] First 500 chars of rendered HTML:", html[:500])
            text = await page.inner_text("body")
            html = html +"\n" + text
            await asyncio.sleep(2)  # give JS and dynamic content time to load
            html = await page.content()
            print(f"[INFO] Rendered page fetched for {url} ({len(html)} chars)")
            return html
        except Exception as e:
            print(f"[ERROR] Failed to load {url}: {e}")
            return ""
        finally:
            await browser.close()