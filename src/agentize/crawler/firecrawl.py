from dataclasses import dataclass

from agents import RunContextWrapper
from agents import function_tool
from firecrawl import FirecrawlApp


@dataclass
class FirecrawlAuth:
    token: str


def scrape(wrapper: RunContextWrapper[FirecrawlAuth], url: str) -> str:
    """Scrape and the content from the given URL.

    Args:
        url (str): The URL to scrape.
    """
    app = FirecrawlApp(api_key=wrapper.context.token)

    result = app.scrape_url(url, formats=["markdown"])
    if not result.success:
        raise Exception(f"Failed to load URL: {url}, got: {result.error}")

    return result.markdown


def search(wrapper: RunContextWrapper[FirecrawlAuth], url: str) -> str:
    """Search and the content from the given URL.

    Args:
        url (str): The URL to scrape.
    """
    app = FirecrawlApp(api_key=wrapper.context.token)

    result = app.search(url, limit=3)
    if not result.success:
        raise Exception(f"Failed to load URL: {url}, got: {result.error}")

    return result.markdown


scrape_tool = function_tool(scrape)
