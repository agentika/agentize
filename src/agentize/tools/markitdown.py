from __future__ import annotations

import requests
import ua_generator
from agents import function_tool
from loguru import logger
from markitdown import MarkItDown

from .firecrawl import fc_scrape


def scrape(url: str) -> str:
    """Scrape the content from the given URL. This is faster than the fc_scrape_tool.

    Args:
        url (str): The URL to scrape.
    """
    user_agent = ua_generator.generate(
        device="desktop",
        platform=("windows", "macos"),
        browser=("chrome", "edge", "firefox", "safari"),
    )
    requests_session = requests.Session()
    requests_session.headers.update(user_agent.headers.get())
    md = MarkItDown(enable_plugins=False, requests_session=requests_session)
    try:
        result = md.convert_url(url)
        result_md = result.markdown
    except requests.exceptions.HTTPError:
        logger.info(f"Fallback: failed to scrape {url} with MarkItDown, using fc_scrape")
        result_md = fc_scrape(url)

    return result_md


scrape_tool = function_tool(scrape)
