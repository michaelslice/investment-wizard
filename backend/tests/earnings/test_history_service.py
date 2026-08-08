from datetime import UTC, date, datetime

from src.earnings.history_service import EarningsHistoryService


class StubClient:
    def get_history(self, symbol: str, limit: int):
        return [{
            "reportDate": datetime(2026, 1, 1, tzinfo=UTC), "timing": "After market close",
            "beforeSessionDate": datetime(2026, 1, 1, tzinfo=UTC), "beforeClose": 100,
            "nextSessionDate": datetime(2026, 1, 2, tzinfo=UTC), "nextOpen": 105,
            "change": 5, "changePercent": 5, "profitOn100Shares": 500,
            "epsEstimate": 1, "reportedEps": 1.1, "surprisePercent": 10,
        }]

    def get_reaction_chart(self, symbol, before_session, next_session, trading_days):
        return [{
            "timestamp": datetime(2026, 1, 1, 15, tzinfo=UTC), "open": 99,
            "high": 101, "low": 98, "close": 100, "volume": 1000,
        }]


async def test_history_summary() -> None:
    result = await EarningsHistoryService(StubClient(), 60).get_history("AAPL", 12)
    assert result.average_change_percent == 5
    assert result.positive_reactions == 1


async def test_reaction_chart() -> None:
    service = EarningsHistoryService(StubClient(), 60)
    chart = await service.get_reaction_chart(
        "AAPL", date(2026, 1, 1), date(2026, 1, 2), 7
    )
    assert chart.points[0].close == 100
    assert chart.trading_days == 7
    assert chart.interval == "Hourly"
