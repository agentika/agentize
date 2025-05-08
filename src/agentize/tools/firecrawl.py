from __future__ import annotations

import os

from agents import function_tool
from firecrawl import FirecrawlApp


def fc_scrape(url: str) -> str:
    """Scrape the content from the given URL using the Firecrawl API. Slower than the scrape_tool.

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


def map(url: str) -> list[str] | None:
    """Crawl a given URL and return all discovered URLs on the page.

    This function uses the Firecrawl API to extract all URLs found on the specified website.
    If the mapping fails, an exception is raised with the error message.

    Args:
        url (str): The target URL to crawl.

    Returns:
        list[str] | None: A list of discovered URLs if successful; None otherwise.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY", "")
    app = FirecrawlApp(api_key=api_key)

    map_result = app.map_url(url)
    if not map_result.success:
        raise Exception(f"Failed to map URL: {url}, got: {map_result.error}")

    return map_result.links


fc_scrape_tool = function_tool(fc_scrape)
search_tool = function_tool(search)
map_tool = function_tool(map)
