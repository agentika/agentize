from functools import cache

import chainlit as cl
from agents import Agent
from agents import ModelSettings
from agents import Runner
from agents import TResponseInputItem
from agents import function_tool
from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.model import get_openai_model
from agentize.tools.firecrawl import search
from agentize.tools.markitdown import markitdown_scrape_tool
from agentize.utils import configure_langfuse

PROMPT = """
# Role and Objective
你是一位專門協助使用者探索全科宏瑋（hwchiu）網站內容的智能助手，熟悉他在 [hwchiu.com](https://hwchiu.com) 上所有技術文章的內容與風格。你擅長自動化工作流程，幫助使用者從搜尋到精讀，全面掌握 hwchiu 的技術觀點。

你的任務是：
1. 使用 `search_hwchiu_blog` 根據使用者需求主題搜尋相關文章。
2. 對搜尋到的每篇文章，自動使用 `markitdown_scrape` 取得 Markdown 原始內容。
3. 從每篇文章內容中萃取摘要、技術重點與建議閱讀對象，幫助使用者快速吸收重點資訊。

# Instructions

## 自動化搜尋與摘要流程
- 當使用者輸入任何技術主題或關鍵字（如 Kubernetes、Golang、BPF 等），你應該立即：
  1. 使用 `search_hwchiu_blog` 搜尋相關文章。
  2. 對每篇搜尋結果，使用 `markitdown_scrape` 自動抓取其 Markdown 原文。
  3. 根據內容撰寫摘要與分析。
- 不需等候使用者點選文章才抓取內容，應主動完成整套流程。

## 每篇文章應產出以下格式摘要：
- **標題與連結**：超連結形式呈現。
- **主題摘要**：用 2–4 句簡要說明這篇文章的主旨。
- **技術要點整理**：
  - 架構、流程、步驟
  - 實作技巧或常見陷阱
- **推薦對象**：初學者、實作導向讀者、進階工程師等

## 工具行為規則
- `search_hwchiu_blog` 用於根據主題搜尋多篇相關文章。
- `markitdown_scrape` 用於每篇搜尋結果的網址，不可省略。
- 若工具失敗或網頁格式異常，應清楚說明原因並給出下一步建議。

# Reasoning Steps / Workflow
1. **解析技術主題**：明確了解使用者想學習的方向或問題。
2. **搜尋相關文章**：使用 `search_hwchiu_blog` 搜尋。
3. **對所有搜尋結果抓文**：對每篇搜尋結果呼叫 `markitdown_scrape`。
4. **逐篇產出摘要**：針對每篇文章萃取主題摘要與技術重點。
5. **彙整回傳資訊**：以列表方式呈現所有摘要，供使用者深入閱讀。
6. **支援後續延伸查詢**：若使用者想深入某篇或擴展主題，持續支援。
""".strip()  # noqa: E501


@function_tool
def search_hwchiu_blog(query: str) -> str:
    """Use this function to search for blog posts on hwchiu.com.

    Every query will be prefixed with "hwchiu.com" to ensure that the search is limited to the blog.

    Args:
        query (str): The query to search for.
    """
    return str(search(query=f"hwchiu.com {query}"))


class OpenAIAgent:
    def __init__(self) -> None:
        self.agent = Agent(
            name="main_agent",
            model=get_openai_model(),
            model_settings=ModelSettings(
                temperature=0.1,
                tool_choice="required",
                parallel_tool_calls=True,
            ),
            instructions=PROMPT,
            tools=[markitdown_scrape_tool, search_hwchiu_blog],
        )
        self.messages: list[TResponseInputItem] = []

    async def run(self, message: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )
        result = await Runner.run(starting_agent=self.agent, input=self.messages)
        self.messages = result.to_input_list()
        return str(result.final_output)


@cache
def get_agent() -> OpenAIAgent:
    load_dotenv(find_dotenv(), override=True)
    configure_langfuse(service_name="hwchiu-agent")
    return OpenAIAgent()


@cl.on_message
async def chat(message: cl.Message) -> None:
    agent = get_agent()
    content = await agent.run(message.content)
    await cl.Message(content=content).send()
