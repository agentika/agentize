import os

from agents import function_tool
from firecrawl import FirecrawlApp


@function_tool
async def scrape(url: str) -> str:
    """Scrape and the content from the given URL.

    Args:
        url (str): The URL to scrape.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY", "")
    app = FirecrawlApp(api_key=api_key)

    result = app.scrape_url(url, formats=["markdown"])
    if not result.success:
        raise Exception(f"Failed to load URL: {url}, got: {result.error}")

    return result.markdown
