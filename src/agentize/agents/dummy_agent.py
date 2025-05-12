from agents import Agent
from agents import Model
from agents import ModelSettings

from ..model import get_openai_model


def get_dummy_agent(
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
) -> Agent:
    if model is None:
        model = get_openai_model()

    return Agent(
        name="dummy_agent",
        instructions="You are a dummy agent. Do nothing.",
        model=model,
    )
