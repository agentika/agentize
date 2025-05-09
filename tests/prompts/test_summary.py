from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from agentize.prompts import summarize
from agentize.prompts.summary import Reasoning
from agentize.prompts.summary import Step
from agentize.prompts.summary import Summary


@pytest.mark.asyncio
async def test_summarize() -> None:
    summary = "This is a summary."
    insights = ["Insight 1", "Insight 2", "Insight 3"]
    hashtags = ["#Test", "#Summary", "#UnitTest"]

    with patch("agentize.prompts.summary.lazy_run", new_callable=AsyncMock) as mock_lazy_run:
        mock_summary = Summary(
            reasoning=Reasoning(
                steps=[Step(explanation="explanation", output="output")],
                final_output="final_output",
            ),
            summary=summary,
            insights=insights,
            hashtags=hashtags,
        )
        mock_lazy_run.return_value = mock_summary

        result = await summarize(text="test text", lang="English", length=100)
        assert isinstance(result, Summary)

        result_str = str(result)
        assert summary in result_str
        for insight in insights:
            assert insight in result_str
        for hashtag in hashtags:
            assert hashtag in result_str
