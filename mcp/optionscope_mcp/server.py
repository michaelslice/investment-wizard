import asyncio
from typing import Any, Literal

from fastmcp import FastMCP

from optionscope_mcp.api_client import OptionScopeApiClient

mcp = FastMCP(
    "OptionScope Market Research",
    instructions=(
        "Read-only stock and option market research tools. Data may be delayed and is not "
        "investment advice. Prefer ticker_research_snapshot for an initial company review, "
        "then use focused tools for deeper event, price, sector, or derivatives analysis."
    ),
)
api = OptionScopeApiClient()


@mcp.tool(tags={"equities", "fundamentals"})
async def get_ticker_research(symbol: str) -> dict[str, Any]:
    """Get a detailed investment dossier with valuation, growth, profitability, balance-sheet,
    cash-flow, ownership, short-interest, trading-range, and analyst metrics for one ticker.
    """
    return await api.get(f"/research/tickers/{symbol.upper()}")


@mcp.tool(tags={"equities", "prices", "earnings"})
async def get_stock_timeline(
    symbol: str,
    period: Literal["6mo", "1y", "3y", "5y", "10y", "max"] = "1y",
) -> dict[str, Any]:
    """Get adjusted daily OHLCV history with reported and upcoming earnings plotted in time."""
    return await api.get(f"/prices/{symbol.upper()}", {"period": period})


@mcp.tool(tags={"options", "derivatives"})
async def get_option_chain(symbol: str, expiration: int | None = None) -> dict[str, Any]:
    """Get the live delayed option chain, expirations, quotes, IV, and published Greeks."""
    params: dict[str, Any] = {"symbol": symbol.upper()}
    if expiration is not None:
        params["expiration"] = expiration
    return await api.get("/options", params)


@mcp.tool(tags={"options", "prices"})
async def get_option_contract_history(contract_symbol: str) -> dict[str, Any]:
    """Get all available daily OHLCV prices since a specific OCC option contract was listed."""
    return await api.get(f"/options/history/{contract_symbol.upper()}")


@mcp.tool(tags={"earnings", "events"})
async def get_upcoming_earnings(symbols: list[str] | None = None) -> dict[str, Any]:
    """Get upcoming earnings dates for the default universe or a supplied ticker list."""
    params = {"symbols": ",".join(symbol.upper() for symbol in symbols)} if symbols else None
    return await api.get("/earnings", params)


@mcp.tool(tags={"earnings", "events"})
async def get_earnings_reactions(symbol: str, limit: int = 12) -> dict[str, Any]:
    """Compare pre-report closes with next-session opens across historical earnings events."""
    return await api.get(f"/earnings/history/{symbol.upper()}", {"limit": limit})


@mcp.tool(tags={"earnings", "prices", "events"})
async def get_earnings_reaction_chart(
    symbol: str,
    before_session: str,
    next_session: str,
    trading_days: Literal[1, 7, 14, 21, 63, 126, 252] = 1,
) -> dict[str, Any]:
    """Get intraday or daily OHLCV bars around one earnings event for reaction analysis."""
    return await api.get(
        f"/earnings/history/{symbol.upper()}/chart",
        {
            "before_session": before_session,
            "next_session": next_session,
            "trading_days": trading_days,
        },
    )


@mcp.tool(tags={"equities", "screening"})
async def list_market_sectors() -> list[dict[str, Any]]:
    """List the S&P 500 universe and all supported GICS sectors with constituent counts."""
    return await api.get("/research/sectors")


@mcp.tool(tags={"equities", "screening", "fundamentals"})
async def screen_market_sector(
    sector: str = "all",
    page: int = 1,
    page_size: int = 25,
    query: str = "",
) -> dict[str, Any]:
    """Screen an S&P 500 sector by live market cap and fundamental metrics. Use sector='all'
    for the whole index; page_size must be between 1 and 50.
    """
    return await api.get(
        f"/research/sectors/{sector}",
        {"page": page, "page_size": page_size, "query": query},
    )


@mcp.tool(tags={"equities", "watchlist", "fundamentals"})
async def get_watchlist_fundamentals(symbols: list[str]) -> list[dict[str, Any]]:
    """Get comparable financial metrics for up to 50 ticker symbols in one call."""
    if not symbols:
        return []
    return await api.get(
        "/research/companies",
        {"symbols": ",".join(symbol.upper() for symbol in symbols[:50])},
    )


@mcp.tool(tags={"equities", "agentic-research"})
async def ticker_research_snapshot(
    symbol: str,
    price_period: Literal["6mo", "1y", "3y", "5y", "10y", "max"] = "1y",
    earnings_limit: int = 8,
) -> dict[str, Any]:
    """Fetch a parallel research packet for an investment agent: company fundamentals,
    price/earnings timeline, and historical earnings reactions. This tool gathers evidence;
    it does not produce a buy or sell recommendation.
    """
    ticker = symbol.upper()
    fundamentals, timeline, earnings = await asyncio.gather(
        api.get(f"/research/tickers/{ticker}"),
        api.get(f"/prices/{ticker}", {"period": price_period}),
        api.get(f"/earnings/history/{ticker}", {"limit": earnings_limit}),
    )
    return {
        "symbol": ticker,
        "fundamentals": fundamentals,
        "priceTimeline": timeline,
        "earningsReactions": earnings,
        "disclaimer": "Research data only; not investment advice.",
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
