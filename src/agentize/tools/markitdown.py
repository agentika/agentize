from __future__ import annotations

import requests
import ua_generator
from agents import function_tool
from markitdown import MarkItDown


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
    markitdown = MarkItDown(enable_plugins=False, requests_session=requests_session)
    result = markitdown.convert_url(url)
    return result.markdown


scrape_tool = function_tool(scrape)
