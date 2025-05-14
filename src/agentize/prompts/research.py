from pydantic import BaseModel

PLANNER_PROMPT = (
    "You are a helpful research assistant. Given a query, come up with a set of web searches"
    "to perform to best answer the query. Output between 5 and 20 terms to query for."
    "The search terms must be in English. Translate to English if needed."
)

SEARCH_PROMPT = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary "
    "itself."
)

WRITER_PROMPT = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some initial research done by a research assistant.
You should first come up with an outline for the report that describes the structure and flow of the report.
Then, generate the report and return that as your final output.
The final output should be in markdown format, and it should be lengthy and detailed. Aim
for 5-10 pages of content, at least {length} words. You will also need to upload the markdown report to an S3 bucket.
Default working language: {lang}
Use the language specified by user in messages as the working language when explicitly provided."""


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""

    publish_link: str
    """The link to the published report on telegraph."""
