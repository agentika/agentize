import os
from functools import cache

import chainlit as cl
from agents import Agent
from agents import ModelSettings
from agents import Runner
from agents import TResponseInputItem
from agents.mcp import MCPServerStdio
from agents.mcp import MCPServerStdioParams
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from agentize.model import get_openai_model


class OpenAIAgent:
    def __init__(self) -> None:
        self.agent = Agent(
            name="agent",
            instructions="You are a helpful assistant.",
            model=get_openai_model(),
            model_settings=ModelSettings(temperature=0.0),
            mcp_servers=[
                MCPServerStdio(
                    params=MCPServerStdioParams(
                        command="npx",
                        args=["-y", "firecrawl-mcp"],
                        env={"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY", "")},
                    ),
                )
            ],
        )
        self.messages: list[TResponseInputItem] = []

    async def connect(self) -> None:
        logger.info("Connecting to MCP server...")
        for server in self.agent.mcp_servers:
            await server.connect()

    async def cleanup(self) -> None:
        logger.info("Cleaning up MCP server...")
        for server in self.agent.mcp_servers:
            await server.cleanup()

    async def run(self, message: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        result = await Runner.run(starting_agent=self.agent, input=self.messages)
        self.messages = result.to_input_list()

        return str(result.final_output)


@cache
def get_agent() -> OpenAIAgent:
    load_dotenv(find_dotenv(), override=True)
    return OpenAIAgent()


@cl.on_app_startup
async def connect() -> None:
    agent = get_agent()
    await agent.connect()


@cl.on_app_shutdown
async def cleanup() -> None:
    agent = get_agent()
    await agent.cleanup()


@cl.on_message
async def chat(message: cl.Message) -> None:
    agent = get_agent()
    content = await agent.run(message.content)
    await cl.Message(content=content).send()
