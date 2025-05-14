from functools import cache

import chainlit as cl
from agents import Agent
from agents import ModelSettings
from agents import Runner
from agents import TResponseInputItem
from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.model import get_openai_model
from agentize.prompts.meta import META_PROMPT
from agentize.prompts.meta import Prompt


class Bot:
    def __init__(self) -> None:
        self.agent = Agent(
            name="prompt-engineer-expert",
            instructions=META_PROMPT,
            model=get_openai_model(),
            model_settings=ModelSettings(temperature=0.0),
            output_type=Prompt,
        )
        self.input_items: list[TResponseInputItem] = []

    async def run(self, content: str) -> str:
        self.input_items.append(
            {
                "role": "user",
                "content": content,
            }
        )

        result = await Runner.run(
            self.agent,
            input=self.input_items,
        )
        self.input_items = result.to_input_list()

        return str(result.final_output)


@cache
def get_bot() -> Bot:
    load_dotenv(find_dotenv(), override=True)
    return Bot()


@cl.on_message
async def chat(message: cl.Message) -> None:
    bot = get_bot()
    response = await bot.run(message.content)
    await cl.Message(content=response).send()
