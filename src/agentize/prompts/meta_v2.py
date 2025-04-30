from __future__ import annotations

from pydantic import BaseModel

from ..lazy import parse

# https://cookbook.openai.com/examples/gpt4-1_prompting_guide
INSTRUCTIONS = """
You are a prompt engineering expert.
Your task is to rewrite and enhance the given prompt in {lang}.
"""  # noqa: E501


class Example(BaseModel):
    index: int
    input: str
    output: str

    def __str__(self) -> str:
        return f"Example {self.index}:\nInput: {self.input}\nOutput: {self.output}"


class Prompt(BaseModel):
    role: str
    objective: str
    instructions: list[str]
    reasoning_steps: list[str]
    output_format: str
    examples: list[Example]
    notes: list[str]

    def __str__(self) -> str:
        instructions = "\n".join([f"- {instruction}" for instruction in self.instructions])
        reasoning_steps = "\n".join([f"- {step}" for step in self.reasoning_steps])
        examples = "\n".join([str(example) for example in self.examples])
        notes = "\n".join(
            [f"- {note}" for note in self.notes]
            + [
                "- Do not fabricate any information.",
                "- Think step by step.",
            ]
        )
        return "\n\n".join(
            [
                f"You are a {self.role.lower()}.",
                f"Your task is to {self.objective.lower()}.",
                "# Instructions",
                instructions,
                "# Reasoning Steps",
                reasoning_steps,
                "# Output Format",
                self.output_format,
                "# Examples",
                examples,
                "# Notes",
                notes,
            ]
        )


async def improve_prompt_v2(prompt: str, lang: str = "English") -> Prompt:
    return await parse(input=prompt, instructions=INSTRUCTIONS.format(lang=lang), output_type=Prompt)
