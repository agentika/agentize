import asyncio

from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.prompts import scrape_summarize
from agentize.prompts import summarize


def main() -> None:
    load_dotenv(find_dotenv())

    text = (
        "The quick brown fox jumps over the lazy dog. "
        "This is a well-known pangram that contains all the letters of the English alphabet."
    )
    summary = asyncio.run(summarize(text=text, lang="台灣中文", length=1_000))
    print(summary)

    url_summary = asyncio.run(scrape_summarize(url="https://firecrawl.dev", lang="台灣中文", length=1_000))
    print(url_summary)


if __name__ == "__main__":
    main()
