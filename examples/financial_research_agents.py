from __future__ import annotations

import asyncio
from collections.abc import Sequence
from functools import cache

import chainlit as cl
from agents import Agent
from agents import ModelSettings
from agents import Runner
from agents import RunResult
from agents import Tool
from agents import trace
from aiolimiter import AsyncLimiter
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from agentize.agents import get_dummy_agent
from agentize.model import get_openai_model
from agentize.prompts.financial_research import FINANCIALS_PROMPT
from agentize.prompts.financial_research import PLANNER_PROMPT
from agentize.prompts.financial_research import RISK_PROMPT
from agentize.prompts.financial_research import SEARCH_PROMPT
from agentize.prompts.financial_research import VERIFIER_PROMPT
from agentize.prompts.financial_research import WRITER_PROMPT
from agentize.prompts.financial_research import AnalysisSummary
from agentize.prompts.financial_research import FinancialReportData
from agentize.prompts.financial_research import FinancialSearchItem
from agentize.prompts.financial_research import FinancialSearchPlan
from agentize.prompts.financial_research import VerificationResult
from agentize.tools.boto3 import upload_markdown_tool

# from agentize.tools.duckduckgo import duckduckgo_search
from agentize.tools.firecrawl import search_tool
from agentize.utils import configure_langfuse


async def _summary_extractor(run_result: RunResult) -> str:
    """Custom output extractor for sub‑agents that return an AnalysisSummary."""
    # The financial/risk analyst agents emit an AnalysisSummary with a `summary` field.
    # We want the tool call to return just that summary text so the writer can drop it inline.
    return str(run_result.final_output.summary)


# This is a simple financial research example that uses the agentize library to perform web searches and write reports.
# reference to https://github.com/openai/openai-agents-python/tree/main/examples/financial_research_agent
class ResearchManager:
    def __init__(self) -> None:
        self.final_report: str = ""
        self.report: FinancialReportData = FinancialReportData(
            short_summary="",
            markdown_report="",
            follow_up_questions=[],
        )
        # allow for 5 concurrent entries within a 1 minute window
        self.rate_limit = AsyncLimiter(5)

    def _write_md_report(self) -> None:
        """Write the report to a file."""
        with open("report.md", "w") as f:
            f.write(self.report.markdown_report)

    async def run(self, query) -> str:
        with trace("research workflow"):
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            self.report = await self._write_report(query, search_results)
            verification = await self._verify_report(self.report)

        logger.info(f"=== Follow up questions: {self.report.follow_up_questions}")
        logger.info(f"=== Verification: {verification}")

        self.final_report = f"Report summary\n\n{self.report.short_summary}"
        self._write_md_report()
        return f"{self.final_report}"

    async def _plan_searches(self, query: str) -> FinancialSearchPlan:
        planner_agent = Agent(
            name="financial_planner_agent",
            instructions=PLANNER_PROMPT,
            model=get_openai_model("o3-mini", api_type="chat_completions"),
            output_type=FinancialSearchPlan,
        )

        result = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output_as(FinancialSearchPlan)

    async def _perform_searches(self, search_plan: FinancialSearchPlan) -> Sequence[str]:
        logger.info(f"Got {len(search_plan.searches)} financial search plans.")
        tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
        results: list[str] = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
        return results

    async def _search(self, item: FinancialSearchItem) -> str | None:
        input_data = f"Search term: {item.query}\nReason: {item.reason}"
        search_agent = Agent(
            name="financial_search_agent",
            instructions=SEARCH_PROMPT,
            tools=[search_tool],
            model=get_openai_model("gpt-4.1"),
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

    async def _write_report(self, query: str, search_results: Sequence[str]) -> FinancialReportData:
        fundamentals_tool = summary_agent_tool(
            agent="fundamentals_analyst",
            instructions=FINANCIALS_PROMPT,
            name="fundamentals_analysis",
            description="Use to get a short write‑up of key financial metrics",
        )

        risk_tool = summary_agent_tool(
            agent="fundamentals_analyst",
            instructions=RISK_PROMPT,
            name="risk_analysis",
            description="Use to get a short write‑up of potential red flags",
        )
        writer_with_tools = Agent(
            name="writer_agent",
            instructions=WRITER_PROMPT.format(lang="台灣繁體中文"),
            model=get_openai_model("o3-mini", api_type="chat_completions"),
            tools=[fundamentals_tool, risk_tool, upload_markdown_tool],
            model_settings=ModelSettings(tool_choice="required"),
            output_type=FinancialReportData,
        )
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        logger.info(f"Search plan: {input.replace('\n', '; ')}")
        result = await Runner.run(writer_with_tools, input)
        return result.final_output_as(FinancialReportData)

    async def _verify_report(self, report: FinancialReportData) -> VerificationResult:
        verifier_agent = Agent(
            name="verification_agent",
            instructions=VERIFIER_PROMPT,
            model=get_openai_model("o3-mini", api_type="chat_completions"),
            output_type=VerificationResult,
        )

        result = await Runner.run(verifier_agent, report.markdown_report)
        return result.final_output_as(VerificationResult)


def summary_agent_tool(agent: str, instructions: str, name: str, description: str) -> Tool:
    """Return the agent as a tool."""
    # Expose the specialist analysts as tools so the writer can invoke them inline
    # and still produce the final FinancialReportData output.
    return (
        get_dummy_agent()
        .clone(
            name=f"{agent}_agent",
            instructions=instructions,
            output_type=AnalysisSummary,
        )
        .as_tool(
            tool_name=name,
            tool_description=description,
            custom_output_extractor=_summary_extractor,
        )
    )


@cache
def get_financial_research_manager() -> ResearchManager:
    load_dotenv(find_dotenv(), override=True)
    configure_langfuse(service_name="financial research manager")
    return ResearchManager()


@cl.on_message
async def chat(message: cl.Message) -> None:
    financial_research_manager = get_financial_research_manager()
    content = await financial_research_manager.run(message.content)
    await cl.Message(content=content).send()
