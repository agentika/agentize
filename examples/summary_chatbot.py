from functools import cache

import chainlit as cl
from agents import Agent
from agents import Runner
from agents import TResponseInputItem
from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.agents import get_summary_agent
from agentize.model import get_openai_model
from agentize.tools.duckduckgo import duckduckgo_search
from agentize.tools.firecrawl import map_tool
from agentize.tools.markitdown import markitdown_scrape_tool
from agentize.utils import configure_langfuse


class OpenAIAgent:
    def __init__(self, lang: str = "台灣中文", length: int = 200) -> None:
        self.summary_agent = get_summary_agent(
            lang=lang,
            length=length,
            model=get_openai_model(model="o3-mini", api_type="chat_completions"),
        )
        self.main_agent = Agent(
            name="main_agent",
            model=get_openai_model(),
            instructions="You are a helpful assistant. Handoff to the summary agent when you need to summarize.",
            tools=[markitdown_scrape_tool, map_tool, duckduckgo_search],
            handoffs=[self.summary_agent],
        )
        self.messages: list[TResponseInputItem] = []

    async def run(self, message: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )
        result = await Runner.run(starting_agent=self.main_agent, input=self.messages)
        self.messages = result.to_input_list()
        return str(result.final_output)


@cache
def get_agent() -> OpenAIAgent:
    load_dotenv(find_dotenv(), override=True)
    configure_langfuse(service_name="summary agent")
    return OpenAIAgent()


@cl.on_message
async def chat(message: cl.Message) -> None:
    agent = get_agent()
    content = await agent.run(message.content)
    await cl.Message(content=content).send()
