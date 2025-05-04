from __future__ import annotations

import os

from agents import function_tool
from firecrawl import FirecrawlApp


def scrape(url: str) -> str:
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


def search(query: str) -> list[dict[str, str]]:
    """Perform a web search.
    This function sends the given query to the Firecrawl API and returns the top 3 results.
    If the search fails, it raises an exception with the error message.

    Args:
        query (str): The search keyword.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY", "")
    app = FirecrawlApp(api_key=api_key)

    search_result = app.search(query, limit=3)
    if not search_result.success:
        raise Exception(f"Failed to search keyword: {query}, got: {search_result.error}")

    return search_result.data


scrape_tool = function_tool(scrape)
search_tool = function_tool(search)
