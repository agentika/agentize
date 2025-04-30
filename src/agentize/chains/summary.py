from __future__ import annotations

from pydantic import BaseModel

from ..lazy import parse

PROMPT_TEMPLATE = """
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

Input:  
{text}
""".strip()  # noqa


class Summary(BaseModel):
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


async def summarize(text: str, lang: str, length: int = 200) -> str:
    return str(
        await parse(
            input=PROMPT_TEMPLATE.format(text=text, lang=lang, length=length),
            output_type=Summary,
        )
    )
