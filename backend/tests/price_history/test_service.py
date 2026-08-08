from datetime import UTC, datetime

from src.price_history.service import PriceHistoryService


class StubClient:
    def get_timeline(self, symbol, period):
        return {"prices": [{"date": datetime(2026, 1, 1, tzinfo=UTC), "open": 99, "high": 102, "low": 98, "close": 101, "volume": 1000}], "earnings": []}


async def test_latest_price() -> None:
    result = await PriceHistoryService(StubClient(), 60).get_timeline("AAPL", "1y")
    assert result.latest_price == 101
