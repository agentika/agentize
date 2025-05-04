import os

from agents import function_tool
from firecrawl import AsyncFirecrawlApp


async def scrape(url: str) -> str:
    """Scrape and the content from the given URL.

    Args:
        url (str): The URL to scrape.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY", "")
    app = AsyncFirecrawlApp(api_key=api_key)

    result = await app.scrape_url(url, formats=["markdown"])

    return result.markdown


scrape_tool = function_tool(scrape)
