from agents import Agent
from agents import Model
from agents import ModelSettings

from ..model import get_openai_model
from ..tools.duckduckgo import duckduckgo_search

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary "
    "itself."
)


def get_search_agent(
    model: Model | None = None,
    model_settings: ModelSettings | None = None,
) -> Agent:
    if model is None:
        model = get_openai_model()

    return Agent(
        name="search_agent",
        instructions=INSTRUCTIONS,
        tools=[duckduckgo_search],
        model=model,
        model_settings=ModelSettings(tool_choice="required"),
    )
