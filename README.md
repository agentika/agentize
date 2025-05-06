# agentize
[![image](https://img.shields.io/pypi/v/agentize.svg)](https://pypi.python.org/pypi/agentize)

Agentize provides out-of-the-box tools for building chatbot agent with LLMs.

## Usage

### Tools

#### Firecrawl

- Scrape tool to scrape a URL and get its content.
- Search tool to perform web searches and optionally retrieve content from the results.
- Map tool to go from a single url to a map of the entire website.

#### Telepragh

- Publish tool to publish content on Telegraph

### Agents

- Summary agent to summarize a document.

## Examples

Chatbot agent

```sh
uv run chainlit run examples/chatbot_agent.py
```

Chatbot with MCP client

```sh
uv run chainlit run examples/mcp_chatbot.py
```

Summarize chatbot

```sh
uv run chainlit run examples/summarize_chatbot.py
```

## Development

type check and format the code

```sh
make format fix type
```

pre-commit git hook installation

```sh
pre-commit install
# or manually run
pre-commit run --all-files
```

### Environment variables

```sh
# OpenAI compatible proxy
# export OPENAI_PROXY_BASE_URL="..."
# export OPENAI_PROXY_API_KEY="..."

# OpenAI
# export OPENAI_MODEL="gpt-4o-mini"
# export OPENAI_API_KEY="sk-..."

# Firecrawl (optional)
export FIRECRAWL_API_KEY="fc-..."

# Langfuse
export LANGFUSE_PUBLIC_KEY="pk-..."
export LANGFUSE_SECRET_KEY="sk-..."
export LANGFUSE_HOST="..."

# Azure OpenAI
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="..."
export OPENAI_MODEL="gpt-4.1"
export OPENAI_API_VERSION="...."
```
