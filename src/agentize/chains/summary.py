from __future__ import annotations

from pydantic import BaseModel

from ..lazy import parse

PROMPT_TEMPLATE = """
Please generate the following in {lang} based on the provided content:

- Summary: Based on a logical analysis of the content, comprehensively and systematically summarize the information, retaining the main points and key details so that the summary fully presents the focus and context of the original content.
- Insights: Use bullet points to present in-depth and clear takeaways, highlighting the main insights, underlying meanings, trends, impacts, or potential follow-up developments found in the content.
- Hashtags: Select and provide at least three relevant and internationally used English hashtags, separated by spaces (e.g., #Technology #Sustainability #Innovation).

## Steps
- Carefully read the original input, precisely identifying the core arguments, concrete information, and key details.
- Combine and organize similar or duplicate information to avoid redundancy, ensuring that highlights stand out and logic is clear. Appropriately preserve examples and background context.
- Express all explanations in {lang} using phrasing and style common in the specified context—be clear, concise, avoid unnecessary details or filler, and enhance readability.
- Both the summary and insights must be translated and written in authentic {lang}, and all content must be grounded in factual information, without adding any unverified details.
- Present the results in the following order: Summary, Insights, Hashtags.

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


async def summarize(text: str, lang: str) -> str:
    return str(
        await parse(
            input=PROMPT_TEMPLATE.format(text=text, lang=lang),
            output_type=Summary,
        )
    )
