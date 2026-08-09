import asyncio
from pathlib import Path

from fastmcp import Client


async def main() -> None:
    server_path = Path(__file__).parent / "optionscope_mcp" / "server.py"
    client = Client(str(server_path))
    async with client:
        tools = await client.list_tools()
        print("Available tools:", [tool.name for tool in tools])
        result = await client.call_tool("get_ticker_research", {"symbol": "AAPL"})
        data = result.data
        print("Result:", data["symbol"], data["name"], data["currentPrice"])


if __name__ == "__main__":
    asyncio.run(main())
