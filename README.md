# agentize
[![image](https://img.shields.io/pypi/v/agentize.svg)](https://pypi.python.org/pypi/agentize)

Agentize provides out-of-the-box tools for building chatbot agent with LLMs.

## Usage

### Installation

```sh
pip install agentize

# If you want to use langfuse
pip install agentize[langfuse]
```

### Tools


#### MarkItDown

- `markitdown_scrape` tool to scrape a URL and get its content.

#### Firecrawl

- `firecrawl_scrape` tool to scrape a URL and get its content.
- `search` tool to perform web searches and optionally retrieve content from the results.
- `map` tool to go from a single url to a map of the entire website.

#### Telegraph

- `publish_page_md` tool to publish a markdown document to telegraph and get its URL.

#### Wise

- `query_rate_history` tool to query the rate history of a currency.

### Agents

- Summary agent to summarize a document.

## Examples

Chatbot agent. Summarize chatbot. The `-w` flag tells Chainlit to enable auto-reloading, so you don’t need to restart the server every time you make changes to your application.

```sh
uv run chainlit run examples/chatbot_agent.py -w
```

Chatbot with MCP client.

```sh
uv run chainlit run examples/mcp_chatbot.py -w
```

Summarize chatbot.

```sh
uv run chainlit run examples/summarize_chatbot.py -w
```

Prompt generation:
```
uv run chainlit run examples/prompt_generation.py -w
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
# OpenAI compatible API
# export OPENAI_BASE_URL="..."
# export OPENAI_API_KEY="..."

# OpenAI
# export OPENAI_MODEL="gpt-4o-mini"
# export OPENAI_API_KEY="sk-..."

# Firecrawl (optional)
export FIRECRAWL_API_KEY="fc-..."

# Object Storage (optional), S3 compatible Storage
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY=".."
export AWS_ENDPOINT_URL_S3="..."
export AWS_BUCKET_NAME="..."

# Langfuse
export LANGFUSE_PUBLIC_KEY="pk-..."
export LANGFUSE_SECRET_KEY="sk-..."
export LANGFUSE_HOST="..."

# Azure OpenAI
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="..."
export OPENAI_MODEL="gpt-4.1"
# see https://learn.microsoft.com/azure/ai-services/openai/api-version-deprecation for more details
export OPENAI_API_VERSION="2025-03-01-preview"
```
