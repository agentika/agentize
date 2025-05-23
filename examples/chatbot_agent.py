from functools import cache

import chainlit as cl
from agents import Agent
from agents import Runner
from agents import TResponseInputItem
from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.model import get_openai_model
from agentize.prompts.summary import summarize_tool
from agentize.tools.markitdown import markitdown_scrape_tool


class OpenAIAgent:
    def __init__(self) -> None:
        self.agent = Agent(
            name="agent",
            model=get_openai_model(),
            tools=[summarize_tool, markitdown_scrape_tool],
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
