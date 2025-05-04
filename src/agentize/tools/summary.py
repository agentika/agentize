from agents import RunContextWrapper
from agents import function_tool

from ..context import UserProfileContext
from ..prompts.summary import Summary
from ..prompts.summary import scrape_summarize
from ..prompts.summary import summarize


@function_tool
async def summarize_tool(wrapper: RunContextWrapper[UserProfileContext], text: str) -> Summary:
    """Summarize the given text.

    Args:
        text (str): The text to summarize.
    """
    return await summarize(text=text, lang=wrapper.context.lang, length=wrapper.context.length)


@function_tool
async def scrape_summarize_tool(wrapper: RunContextWrapper[UserProfileContext], url: str) -> Summary:
    """Scrape and summarize the content from the given URL.

    Args:
        url (str): The url to scrape.
    """
    return await scrape_summarize(url=url, lang=wrapper.context.lang, length=wrapper.context.length)
