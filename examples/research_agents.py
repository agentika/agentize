from __future__ import annotations

import asyncio
from collections.abc import Sequence
from functools import cache

import chainlit as cl
from agents import ModelSettings
from agents import Runner
from agents import trace
from aiolimiter import AsyncLimiter
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from agentize.agents import get_dummy_agent
from agentize.model import get_openai_model
from agentize.prompts.research import PLANNER_PROMPT
from agentize.prompts.research import SEARCH_PROMPT
from agentize.prompts.research import WRITER_PROMPT
from agentize.prompts.research import ReportData
from agentize.prompts.research import WebSearchItem
from agentize.prompts.research import WebSearchPlan
from agentize.tools.boto3 import upload_markdown_tool
from agentize.tools.duckduckgo import duckduckgo_search

# from agentize.tools.firecrawl import search_tool
from agentize.utils import configure_langfuse


# This is a simple research manager that uses the agentize library to perform web searches and write reports.
# reference to https://github.com/openai/openai-agents-python/tree/main/examples/research_bot
class ResearchManager:
    def __init__(self) -> None:
        self.final_report: str = ""
        self.report: ReportData = ReportData(
            short_summary="",
            markdown_report="",
            follow_up_questions=[],
            publish_link="",
        )
        # allow for 5 concurrent entries within a 1 minute window
        self.rate_limit = AsyncLimiter(2)

    def _write_md_report(self) -> None:
        """Write the report to a file."""
        with open("report.md", "w") as f:
            f.write(self.report.markdown_report)

    async def run(self, query) -> str:
        with trace("research workflow"):
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            self.report = await self._write_report(query, search_results)
            logger.info(f"=== Follow up questions: {self.report.follow_up_questions}")

        self.final_report = f"Report summary\n\n{self.report.short_summary}\n\n Report link: {self.report.publish_link}"
        self._write_md_report()
        return self.final_report

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        planner_agent = get_dummy_agent().clone(
            name="planner_agent",
            instructions=PLANNER_PROMPT,
            model=get_openai_model("o3-mini", api_type="chat_completions"),
            output_type=WebSearchPlan,
        )

        result = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> Sequence[str]:
        logger.info(f"Got {len(search_plan.searches)} Web search plans.")
        tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
        results: list[str] = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
        return results

    async def _search(self, item: WebSearchItem) -> str | None:
        input_data = f"Search term: {item.query}\nReason: {item.reason}"
        search_agent = get_dummy_agent().clone(
            name="search_agent",
            instructions=SEARCH_PROMPT,
            tools=[duckduckgo_search],
            model_settings=ModelSettings(tool_choice="required"),
        )
        try:
            async with self.rate_limit:
                # this section is *at most* going to entered 5 times
                logger.info("-------------- Search Now -------------------")
                result = await Runner.run(search_agent, input_data)
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, query: str, search_results: Sequence[str]) -> ReportData:
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        logger.info(f"Search plan: {input.replace('\n', '; ')}")
        writer_agent = get_dummy_agent().clone(
            name="writer_agent",
            instructions=WRITER_PROMPT.format(lang="台灣繁體中文", length=1000),
            model=get_openai_model("o3-mini", api_type="chat_completions"),
            tools=[upload_markdown_tool],
            model_settings=ModelSettings(tool_choice="required"),
            output_type=ReportData,
        )
        result = await Runner.run(writer_agent, input)
        return result.final_output_as(ReportData)


@cache
def get_research_manager() -> ResearchManager:
    load_dotenv(find_dotenv(), override=True)
    configure_langfuse(service_name="research manager")
    return ResearchManager()


@cl.on_message
async def chat(message: cl.Message) -> None:
    research_manager = get_research_manager()
    content = await research_manager.run(message.content)
    await cl.Message(content=content).send()
