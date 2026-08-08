from src.research.service import ResearchService


class StubClient:
    def get_company(self, symbol: str):
        return {
            "symbol": symbol, "name": symbol, "sector": "Technology", "industry": "Software",
            "marketCap": 2 if symbol == "AAPL" else 1, "currentPrice": 100,
            "trailingPe": 20, "revenue": 10, "profitMargin": .2,
            "targetPrice": 120, "recommendation": "buy",
        }


async def test_sector_companies_are_ranked_by_market_cap(monkeypatch) -> None:
    monkeypatch.setitem(__import__("src.research.constants", fromlist=["SECTOR_SYMBOLS"]).SECTOR_SYMBOLS, "test", ("MSFT", "AAPL"))
    monkeypatch.setitem(__import__("src.research.constants", fromlist=["SECTOR_LABELS"]).SECTOR_LABELS, "test", "Test")
    result = await ResearchService(StubClient(), 60).get_sector("test")
    assert [company.symbol for company in result.companies] == ["AAPL", "MSFT"]
