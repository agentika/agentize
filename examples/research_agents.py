import asyncio
from functools import cache

import chainlit as cl
from agents import Runner
from agents import trace
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from agentize.agents import get_planner_agent
from agentize.agents import get_search_agent
from agentize.agents import get_writer_agent
from agentize.agents.planner_agent import WebSearchPlan
from agentize.agents.writer_agent import ReportData
from agentize.model import get_openai_model
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

    def _write_md_report(self) -> None:
        """Write the report to a file."""
        with open("report.md", "w") as f:
            f.write(self.report.markdown_report)

    async def run(self, query) -> str:
        with trace("research workflow"):
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            self.report = await self._write_report(query, search_results)
            logger.info(f"Follow up questions: {self.report.follow_up_questions}")

        self.final_report = f"Report summary\n\n{self.report.short_summary}\n\n Report link: {self.report.publish_link}"
        self._write_md_report()
        return self.final_report

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        result = await Runner.run(
            get_planner_agent(model=get_openai_model("o3-mini", api_type="chat_completions")),
            f"Query: {query}",
        )
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        search_results = []
        logger.info(f"Got {len(search_plan.searches)} Web search plans.")
        search_terms_top_5 = search_plan.searches[:5]

        tasks = []
        for item in search_terms_top_5:
            search_term = f"Search term: {item.query}; Reason for searching: {item.reason}"
            logger.info(f"Search term: {search_term}")
            task = Runner.run(get_search_agent(), search_term)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        for r in results:
            if r is not None:
                logger.info(f"Search result: {r.final_output}")
                search_results.append(r.final_output)

        return search_results

    async def _write_report(self, query: str, search_results: list[str]) -> ReportData:
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        logger.info(f"Search plan: {input.replace('\n', '; ')}")
        result = await Runner.run(
            get_writer_agent(
                lang="台灣繁體中文",
                model=get_openai_model("o3-mini", api_type="chat_completions"),
            ),
            input,
        )
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
