from typing import TypeVar

from agents import Agent
from agents import Model
from agents import ModelSettings
from agents import Runner
from pydantic import BaseModel

from .model import get_openai_model
from .model import get_openai_model_settings

TextFormatT = TypeVar("TextFormatT", bound=BaseModel)


async def lazy_run(
    input: str,
    instructions: str | None = None,
    name: str = "lazy_run",
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
    output_type: type[TextFormatT] | None = None,
) -> str | TextFormatT:
    """Run the agent with the given input and instructions.

    Args:
        input (str): The input to the agent.
        instructions (str | None): The instructions for the agent.
        name (str): The name of the agent.
        model (Model | None): The model to use for the agent.
        model_settings (ModelSettings | None): The settings for the model.
        output_type (type[TextFormatT] | None): The type of output to return.
    """
    if model is None:
        model = get_openai_model()

    if model_settings is None:
        model_settings = get_openai_model_settings()

    result = await Runner.run(
        starting_agent=Agent(
            name=name,
            instructions=instructions,
            model=model,
            model_settings=model_settings,
            output_type=output_type,
        ),
        input=input,
    )

    if output_type is None:
        return result.final_output
    return result.final_output_as(output_type)


async def send(input: str, instructions: str | None = None) -> str:
    result = await Runner.run(
        starting_agent=Agent(
            "lazy_send_agent",
            instructions,
            model=get_openai_model(),
            model_settings=get_openai_model_settings(),
        ),
        input=input,
    )
    return result.final_output


async def parse(
    input: str, output_type: type[TextFormatT], instructions: str | None = None
) -> TextFormatT:
    result = await Runner.run(
        starting_agent=Agent(
            "lazy_parse_agent",
            instructions,
            model=get_openai_model(),
            model_settings=get_openai_model_settings(),
            output_type=output_type,
        ),
        input=input,
    )
    return result.final_output
