# agentize
[![image](https://img.shields.io/pypi/v/agentize.svg)](https://pypi.python.org/pypi/agentize)

Agentize provides out-of-the-box tools for building chatbot agent with LLMs.

## Usage

### Installation

```sh
pip install agentize

# If you want to use langfuse
pip install agentize[langfuse]

# If you want to use markitdown
pip install agentize[markitdown]

# Or just install all the extras
pip install agentize[all]
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

# Gemini (Google Generative AI)
export OPENAI_API_KEY="GOOGLE_API_KEY"
export OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export OPENAI_MODEL="gemini-2.0-flash"
export OPENAI_AGENTS_DISABLE_TRACING=1 # (Optional) Disable tracing provided by the OpenAI SDK

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

We follow the same environment variable conventions used by the official OpenAI and Azure OpenAI SDKs. This ensures a seamless integration experience and consistency across environments. The only difference is that if the environment variable AZURE_OPENAI_API_KEY is present, AzureOpenAI will be used. Below is a list of supported environment variables for each client, along with their descriptions and usage examples.

#### OpenAI / AsyncOpenAI
| Variable Name       | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `OPENAI_API_KEY`    | ✅ Required. Your OpenAI API key                      |
| `OPENAI_ORG_ID`     | 🟡 Optional. Organization ID                         |
| `OPENAI_PROJECT_ID` | 🟡 Optional. Project ID                              |
| `OPENAI_BASE_URL`   | 🟡 Optional. Custom base URL (e.g., for proxy usage) |

#### AzureOpenAI / AsyncAzureOpenAI

| Variable Name           | Description                                                                 |
| ----------------------- | --------------------------------------------------------------------------- |
| `AZURE_OPENAI_API_KEY`  | ✅ Required if not using AD token. Azure OpenAI API key                      |
| `AZURE_OPENAI_AD_TOKEN` | ✅ Required if not using API key. Azure Active Directory token               |
| `OPENAI_API_VERSION`    | ✅ Required. API version, e.g., `2025-03-01-preview`                         |
| `AZURE_OPENAI_ENDPOINT` | ✅ Required. Azure endpoint (e.g., `https://your-resource.openai.azure.com`) |
| `OPENAI_ORG_ID`         | 🟡 Optional. Organization ID (for compatibility)                            |
| `OPENAI_PROJECT_ID`     | 🟡 Optional. Project ID (for compatibility)                                 |

#### OpenAI Compatible API / AsyncOpenAI

| Variable Name       | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `OPENAI_API_KEY`    | ✅ Required. Your OpenAI API key                     |
| `OPENAI_BASE_URL`   | ✅ Required. Custom base URL (e.g., for proxy usage) |

### Using OpenAI compatible API

To use an OpenAI compatible API (like [Gemini](https://ai.google.dev/gemini-api/docs/openai)), you can use the `get_openai_model` function to change the API type to `chat_completions` and set the model accordingly. Here's an example of how to do this:

```
self.agent = Agent(
    ...
    model=get_openai_model(api_type="chat_completions"),

# or if you want to use a specific model (Override the OPENAI_MODEL environment variable):
self.agent = Agent(
    ...
    model=get_openai_model(model="gemini-2.0-flash", api_type="chat_completions"),
```
