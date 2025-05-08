from typing import Any

from agents import function_tool
from ytelegraph import TelegraphAPI


@function_tool
def publish_page_md(title: str, content: str) -> str:
    """Publish a new Telegraph page with Markdown content.

    Args:
        title (str): The title of the page.
        content (str): The content of the page in Markdown format.

    Returns:
        url (str): The URL of the created page.
    """
    ph = TelegraphAPI()
    return ph.create_page_md(title, content)


@function_tool
def publish_page(title: str, content: list[dict[str, Any]]) -> str:
    """Publish a Telegraph page with DOM-based format content.

    Args:
        title (str): The title of the page.
        content (list[dict[str, Any]]): The content of the page in Telegraph node format.

    Returns:
        url (str): The URL of the published page.

    Note:
        Use the `publish_page_md` method for Markdown content.
    """
    ph = TelegraphAPI()
    return ph.create_page(title, content)
