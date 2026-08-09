# OptionScope MCP

Read-only FastMCP server that makes the OptionScope market-data APIs available
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
export OPTIONSCOPE_API_URL=https://your-api.example.com/api
```

## Run over stdio

```bash
.venv/bin/python -m optionscope_mcp.server
```

Or use the FastMCP CLI:

```bash
.venv/bin/fastmcp run optionscope_mcp/server.py:mcp
```

Example MCP host configuration:

```json
{
  "mcpServers": {
    "optionscope": {
      "command": "/absolute/path/options-dashboard/mcp/.venv/bin/python",
      "args": ["-m", "optionscope_mcp.server"],
      "env": {"OPTIONSCOPE_API_URL": "http://127.0.0.1:8000/api"}
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
