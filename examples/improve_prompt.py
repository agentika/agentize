import asyncio

from dotenv import find_dotenv
from dotenv import load_dotenv

from agentize.prompts import improve_prompt


def main() -> None:
    load_dotenv(find_dotenv())

    result = asyncio.run(improve_prompt(prompt="Summarize the following text: {text}", lang="English"))
    print(result)


if __name__ == "__main__":
    main()
