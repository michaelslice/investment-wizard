from src.research.service import ResearchService


class StubClient:
    def get_constituents(self):
        return [
            {"symbol": "MSFT", "name": "Microsoft", "sector": "Test", "industry": "Software"},
            {"symbol": "AAPL", "name": "Apple", "sector": "Test", "industry": "Hardware"},
        ]

    def get_company(self, symbol: str):
        return {
            "symbol": symbol, "name": symbol, "sector": "Technology", "industry": "Software",
            "marketCap": 2 if symbol == "AAPL" else 1, "currentPrice": 100,
            "trailingPe": 20, "revenue": 10, "profitMargin": .2,
            "targetPrice": 120, "recommendation": "buy",
        }

    def get_ticker_research(self, symbol: str):
        return {"symbol": symbol, "name": "Apple", "currentPrice": 100, "marketCap": 2}

    def get_holders(self, symbol: str):
        return [{"name": "Fund A", "shares": 100, "changePercent": 2.5}]


async def test_sector_companies_are_ranked_by_market_cap(monkeypatch) -> None:
    constants = __import__("src.research.constants", fromlist=["GICS_TO_SLUG"])
    monkeypatch.setitem(constants.GICS_TO_SLUG, "Test", "test")
    monkeypatch.setitem(constants.SECTOR_LABELS, "test", "Test")
    result = await ResearchService(StubClient(), 60).get_sector("test")
    assert [company.symbol for company in result.companies] == ["AAPL", "MSFT"]
    assert result.total_count == 2


async def test_ticker_research_is_cached() -> None:
    service = ResearchService(StubClient(), 60)
    first = await service.get_ticker_research("AAPL")
    second = await service.get_ticker_research("AAPL")
    assert first.current_price == 100
    assert second.name == "Apple"


async def test_holders_are_returned() -> None:
    result = await ResearchService(StubClient(), 60).get_holders("AAPL")
    assert result.symbol == "AAPL"
    assert result.holders[0].shares == 100
