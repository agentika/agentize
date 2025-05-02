from __future__ import annotations

from pydantic import BaseModel

from ..lazy import parse

INSTRUCTIONS = """
Please generate the following in {lang} based on the provided content:

- **Summary**: Provide a comprehensive and well-organized summary that captures the core message, main points, and key details of the original content. The summary should reflect the full context and significance of the material. (Recommended maximum length: {length} words)
- **Insights**: List at least three important and in-depth insights or key takeaways using bullet points. Focus on highlighting main observations, underlying meanings, trends, impacts, or potential future developments that emerge from the content. Avoid unfounded speculation—ensure all insights are grounded in the input.
- **Hashtags**: Select at least three relevant, internationally recognized English hashtags that accurately represent the main themes of the content. Separate each hashtag with a space (for example: #Technology #Sustainability #Innovation).

# Guidelines
1. Carefully analyze the original input, identifying the central arguments, supporting information, and critical details.
2. Consolidate or merge similar or duplicate points to reduce redundancy and maintain logical flow. Retain relevant examples and background information where appropriate.
3. Use clear and concise language that is natural and idiomatic for {lang}, following the conventions used in Taiwan (if generating in Traditional Chinese). Eliminate unnecessary filler or over-generalizations to enhance readability.
4. All outputs—summary and insights—must be written in authentic, high-quality {lang}, based solely on factual information from the input. Do not add any unverified or external details.

*Optional: If the subject matter is sensitive or controversial, ensure factual accuracy and neutral tone in your summary and insights.*
"""  # noqa


class Step(BaseModel):
    explanation: str
    output: str


class Reasoning(BaseModel):
    steps: list[Step]
    final_output: str


class Summary(BaseModel):
    reasoning: Reasoning
    summary: str
    insights: list[str]
    hashtags: list[str]

    def __str__(self) -> str:
        insights = "\n".join([f"  • {insight.strip()}" for insight in self.insights])
        hashtags = " ".join(self.hashtags)
        return "\n\n".join(
            [
                "📝 Summary",
                self.summary.strip(),
                "💡 Insights",
                insights,
                f"🏷️ Hashtags: {hashtags}",
            ]
        )


async def summarize(text: str, lang: str, length: int = 200) -> Summary:
    """Summarize the given text in the specified language and length.

    Args:
        text (str): The text to summarize.
        lang (str): The language to use for the summary.
        length (int): The maximum length of the summary in words.
    """
    return await parse(
        input=text,
        instructions=INSTRUCTIONS.format(lang=lang, length=length),
        output_type=Summary,
    )
