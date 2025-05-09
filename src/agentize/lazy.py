from typing import TypeVar

from agents import Agent
from agents import Model
from agents import ModelSettings
from agents import Runner

from .model import get_openai_model

T = TypeVar("T")


def _create_agent(
    instructions: str | None = None,
    name: str = "lazy_run",
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
    output_type: type[T] | None = None,
) -> Agent:
    model = model or get_openai_model()
    model_settings = model_settings or ModelSettings()
    return Agent(
        name=name,
        instructions=instructions,
        model=model,
        model_settings=model_settings,
        output_type=output_type,
    )


async def lazy_run(
    input: str,
    instructions: str | None = None,
    name: str = "lazy_run",
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
    output_type: type[T] | None = None,
) -> T:
    """Run the agent with the given input and instructions.

    Args:
        input (str): The input to the agent.
        instructions (str | None): The instructions for the agent.
        name (str): The name of the agent.
        model (Model | None): The model to use for the agent.
        model_settings (ModelSettings | None): The settings for the model.
        output_type (type[T] | None): The type of output to return.
    """
    model_settings = model_settings or ModelSettings()
    result = await Runner.run(
        starting_agent=_create_agent(
            instructions=instructions,
            name=name,
            model=model,
            model_settings=model_settings,
            output_type=output_type,
        ),
        input=input,
    )

    if output_type is None:
        return result.final_output
    return result.final_output_as(output_type)


def lazy_run_sync(
    input: str,
    instructions: str | None = None,
    name: str = "lazy_run_sync",
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
    output_type: type[T] | None = None,
) -> str | T:
    """Run the agent with the given input and instructions.

    Args:
        input (str): The input to the agent.
        instructions (str | None): The instructions for the agent.
        name (str): The name of the agent.
        model (Model | None): The model to use for the agent.
        model_settings (ModelSettings | None): The settings for the model.
        output_type (type[T] | None): The type of output to return.
    """
    model_settings = model_settings or ModelSettings()
    result = Runner.run_sync(
        starting_agent=_create_agent(
            instructions=instructions,
            name=name,
            model=model,
            model_settings=model_settings,
            output_type=output_type,
        ),
        input=input,
    )

    if output_type is None:
        return result.final_output
    return result.final_output_as(output_type)
