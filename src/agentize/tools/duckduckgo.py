from __future__ import annotations

import json

from agents import function_tool
from duckduckgo_search import DDGS


@function_tool
def duckduckgo_search(query: str) -> str:
    """Perform a web search. Use this function to search DuckDuckGo for a query.

    Args:
        query (str): The query to search for.

    Returns:
        The result from DuckDuckGo.
    """
    ddgs = DDGS()
    return json.dumps(ddgs.text(keywords=query, max_results=5), indent=2)


@function_tool
def duckduckgo_news(query: str) -> str:
    """Use this function to get the latest news from DuckDuckGo.
    Args:
        query(str): The query to search for.

    Returns:
        The latest news from DuckDuckGo.
    """
    ddgs = DDGS()
    return json.dumps(ddgs.news(keywords=query, max_results=5), indent=2)
