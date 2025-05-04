from functools import cache

import chainlit as cl
from agents import Agent
from agents import ModelSettings
from agents import Runner
from agents import TResponseInputItem
from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.agents.summary import get_summary_agent
from agentize.crawler.firecrawl import scrape_tool
from agentize.model import get_openai_model


class OpenAIAgent:
    def __init__(self, lang: str = "台灣中文", length: int = 200) -> None:
        self.summary_agent = get_summary_agent(lang=lang, length=length)
        self.agent = Agent(
            name="agent",
            instructions="You are a helpful assistant. Handoff to the summary agent when you need to summarize.",
            model=get_openai_model(),
            model_settings=ModelSettings(temperature=0.0),
            tools=[scrape_tool],
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
        result = await Runner.run(starting_agent=self.agent, input=self.messages)
        self.messages = result.to_input_list()
        return result.final_output_as(str)


@cache
def get_agent() -> OpenAIAgent:
    load_dotenv(find_dotenv(), override=True)
    return OpenAIAgent()


@cl.on_message
async def chat(message: cl.Message) -> None:
    agent = get_agent()
    content = await agent.run(message.content)
    await cl.Message(content=content).send()
