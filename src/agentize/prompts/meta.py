from __future__ import annotations

from ..lazy import send

# https://cookbook.openai.com/examples/gpt4-1_prompting_guide
INSTRUCTIONS = """
You are a prompt engineering expert.

Your task is to rewrite and enhance the given prompt in {lang}.

# Instructions
1. Identify the goal and desired outcome of the original prompt.
2. Refine the structure for clarity and completeness.
3. Apply the prompt engineering best practices.
4. Ensure the improved prompt explicitly instructs the model or user to “think step by step” when generating the response, to ensure high-quality output.

# Output Format
Return only the improved prompt, with enhanced structure and examples if needed. Do not include any additional commentary.
"""  # noqa: E501


async def improve_prompt(prompt: str, lang: str = "English") -> str:
    return await send(
        input=prompt,
        instructions=INSTRUCTIONS.format(lang=lang),
    )
