from agents import function_tool
from ytelegraph import TelegraphAPI


@function_tool
def publish_page(title: str, content: str) -> str:
    """Publish a new Telegraph page with Markdown content.

    Args:
        title (str): The title of the page.
        content (str): The content of the page in Markdown format.

    Returns:
        url (str): The URL of the created page.
    """
    ph = TelegraphAPI()
    return ph.create_page_md(title, content)
