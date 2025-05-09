from __future__ import annotations

import os
from functools import cache
from typing import Literal

from agents import Model
from agents import ModelSettings
from agents import OpenAIChatCompletionsModel
from agents import OpenAIResponsesModel
from loguru import logger
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI
from openai.types import ChatModel


@cache
def get_openai_client() -> AsyncOpenAI:
    # OpenAI-compatible endpoints
    openai_proxy_api_key = os.getenv("OPENAI_PROXY_API_KEY")
    openai_proxy_base_url = os.getenv("OPENAI_PROXY_BASE_URL")
    if openai_proxy_api_key:
        logger.info("Using OpenAI proxy API key")
        return AsyncOpenAI(base_url=openai_proxy_base_url, api_key=openai_proxy_api_key)

    # Azure OpenAI-comatible endpoints
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if azure_api_key:
        logger.info("Using Azure OpenAI API key")
        return AsyncAzureOpenAI(api_key=azure_api_key)

    logger.info("Using OpenAI API key")
    return AsyncOpenAI()


@cache
def get_openai_model(
    model: ChatModel | str | None = None,
    api_type: Literal["responses", "chat_completions"] = "responses",
) -> Model:
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    openai_client = get_openai_client()

    match api_type:
        case "responses":
            return OpenAIResponsesModel(model, openai_client=openai_client)
        case "chat_completions":
            return OpenAIChatCompletionsModel(model, openai_client=openai_client)
        case _:
            raise ValueError(f"Invalid API type: {api_type}. Use 'responses' or 'chat_completions'.")


@cache
def get_openai_model_settings():
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    temperature = None if model == "o3-mini" else float(os.getenv("OPENAI_TEMPERATURE", 0.0))
    return ModelSettings(temperature=temperature)
