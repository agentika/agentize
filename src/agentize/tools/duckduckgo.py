from __future__ import annotations

import json

from agents import function_tool
from duckduckgo_search import DDGS


@function_tool
def duckduckgo_search(query: str, max_results: int = 5) -> str:
    """Perform a web search. Use this function to search DuckDuckGo for a query.

    Args:
        query (str): The query to search for.
        max_results (optional, default=5): The maximum number of results to return.

    Returns:
        The result from DuckDuckGo.
    """
    ddgs = DDGS()
    return json.dumps(ddgs.text(keywords=query, max_results=max_results), indent=2)


@function_tool
def duckduckgo_news(query: str, max_results: int = 5) -> str:
    """Use this function to get the latest news from DuckDuckGo.
    Args:
        query(str): The query to search for.
        max_results (optional, default=5): The maximum number of results to return.

    Returns:
        The latest news from DuckDuckGo.
    """
    ddgs = DDGS()
    return json.dumps(ddgs.news(keywords=query, max_results=max_results), indent=2)
