# investment-wizard MCP

Read-only FastMCP server that makes the investment-wizard market-data APIs available
to LLM clients and agentic investment-research workflows. The FastAPI service
must be running before these tools are called.

## Install

```bash
cd mcp
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
```

The server targets `http://127.0.0.1:8000/api` by default. Override it with:

```bash
export INVESTMENT_WIZARD_API_URL=https://your-api.example.com/api
```

## Run over stdio

```bash
.venv/bin/python -m investment_wizard_mcp.server
```

Or use the FastMCP CLI:

```bash
.venv/bin/fastmcp run investment_wizard_mcp/server.py:mcp
```

Example MCP host configuration:

```json
{
  "mcpServers": {
    "investment-wizard": {
      "command": "/absolute/path/options-dashboard/mcp/.venv/bin/python",
      "args": ["-m", "investment_wizard_mcp.server"],
      "env": {"INVESTMENT_WIZARD_API_URL": "http://127.0.0.1:8000/api"}
    }
  }
}
```

## Test with the FastMCP client

`client_example.py` uses `import asyncio` and `from fastmcp import Client` to
launch the server over stdio, list its tools, and request an AAPL ticker dossier.

```bash
.venv/bin/python client_example.py
```

Market and analyst data may be delayed, incomplete, or provider-dependent. The
server gathers research evidence and does not issue investment advice.

## Daily market-news digest

The `get_daily_market_news_digest` MCP tool aggregates and deduplicates recent
market coverage across broad-market, macro, rates, sector, earnings, and deal
topics. Calling it again retrieves an updated digest for the LLM to summarize.

To poll the tool continuously from a terminal:

```bash
mcp/.venv/bin/python mcp/market_news_watch.py --interval 15
```

For one update only:

```bash
mcp/.venv/bin/python mcp/market_news_watch.py --once
```
