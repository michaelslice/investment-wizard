import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path

from fastmcp import Client


async def watch(interval_minutes: int, once: bool, max_articles: int) -> None:
    server = Path(__file__).parent / "investment_wizard_mcp" / "server.py"
    async with Client(str(server)) as client:
        while True:
            result = await client.call_tool(
                "get_daily_market_news_digest",
                {"lookback_hours": 24, "max_articles": max_articles},
            )
            print(f"\n=== Market news update {datetime.now().astimezone().isoformat()} ===")
            print(json.dumps(result.data, indent=2, default=str))
            if once:
                return
            await asyncio.sleep(interval_minutes * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Continuously poll the investment-wizard news MCP tool")
    parser.add_argument("--interval", type=int, default=15, help="Refresh interval in minutes")
    parser.add_argument("--max-articles", type=int, default=80)
    parser.add_argument("--once", action="store_true", help="Fetch one digest and exit")
    args = parser.parse_args()
    asyncio.run(watch(max(1, args.interval), args.once, max(10, min(200, args.max_articles))))


if __name__ == "__main__":
    main()
