from agents import Agent
from agents import Model
from agents import ModelSettings
from pydantic import BaseModel

from ..model import get_openai_model
from ..tools.boto3 import upload_markdown_tool

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some initial research done by a research assistant.
You should first come up with an outline for the report that describes the structure and flow of the report.
Then, generate the report and return that as your final output.
The final output should be in markdown format, and it should be lengthy and detailed. Aim
for 5-10 pages of content, at least {length} words. You will also need to upload the markdown report to an S3 bucket.
Default working language: {lang}
Use the language specified by user in messages as the working language when explicitly provided."""


class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""

    publish_link: str
    """The link to the published report on telegraph."""


def get_writer_agent(
    lang: str,
    length: int = 1000,
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
) -> Agent:
    if model is None:
        model = get_openai_model()

    return Agent(
        name="writer_agent",
        instructions=INSTRUCTIONS.format(lang=lang, length=length),
        model=model,
        tools=[upload_markdown_tool],
        model_settings=ModelSettings(tool_choice="required"),
        output_type=ReportData,
    )
