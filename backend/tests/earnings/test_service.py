from datetime import UTC, datetime

from src.earnings.service import EarningsService


class StubClient:
    def get_dates(self, symbol: str):
        return [datetime(2026, 9, 1 if symbol == "AAPL" else 2, tzinfo=UTC)]


async def test_calendar_is_sorted_and_counted() -> None:
    calendar = await EarningsService(StubClient(), 60).get_calendar(("MSFT", "AAPL"))
    assert [event.symbol for event in calendar.events] == ["AAPL", "MSFT"]
    assert calendar.matched_symbols == 2
