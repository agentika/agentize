# agentize
[![image](https://img.shields.io/pypi/v/agentize.svg)](https://pypi.python.org/pypi/agentize)

Agentize provides out-of-the-box tools for building chatbot agent with LLMs.

## Usage

### Crawler

- Scrape tool to scrape a URL and get its content.
- Search tool to perform web searches and optionally retrieve content from the results.
- Map tool to go from a single url to a map of the entire website.

### Agents

- Summary agent to summarize a document.

## Examples

Chatbot agent

```sh
uv run chainlit run examples/chatbot_agent.py
```

Chatbot with MCP client

```sh
uv run chainlit run examples/chatbot_agent.py
```

## Development

type check and format the code

```
make format fix type  
```
