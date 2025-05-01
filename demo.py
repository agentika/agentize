from functools import cache

import chainlit as cl
from agents import Agent
from agents import ModelSettings
from agents import Runner
from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.model import get_openai_model


class OpenAIAgent:
    def __init__(self) -> None:
        self.agent = Agent(
            name="agent",
            model=get_openai_model(),
            model_settings=ModelSettings(temperature=0.0),
        )
        self.messages = []

    async def run(self, message: str) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )
        result = await Runner.run(starting_agent=self.agent, input=self.messages)
        self.messages = result.to_input_list()
        return result.final_output


@cache
def get_agent() -> OpenAIAgent:
    load_dotenv(find_dotenv(), override=True)
    return OpenAIAgent()


@cl.on_message
async def chat(message: cl.Message) -> None:
    agent = get_agent()
    content = await agent.run(message.content)
    await cl.Message(content=content).send()
