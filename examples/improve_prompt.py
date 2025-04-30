import asyncio

from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.prompts import improve_prompt
from agentize.prompts import improve_prompt_v2


def main() -> None:
    load_dotenv(find_dotenv())

    prompt = "Summarize the following text: {text}"

    result = asyncio.run(improve_prompt(prompt=prompt, lang="English"))
    print(result)

    print("=" * 100)

    result = asyncio.run(improve_prompt_v2(prompt=prompt, lang="English"))
    print(result)


if __name__ == "__main__":
    main()
