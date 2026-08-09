from datetime import UTC, datetime

import pytest

from src.options.history_service import OptionHistoryService


class StubHistoryClient:
    calls = 0

    def get_history(self, contract_symbol: str):
        self.calls += 1
        return [{
            "date": datetime(2026, 1, 2, tzinfo=UTC),
            "open": 1.0,
            "high": 1.4,
            "low": 0.9,
            "close": 1.25,
            "volume": 100,
        }]


@pytest.mark.asyncio
async def test_returns_and_caches_contract_history() -> None:
    client = StubHistoryClient()
    service = OptionHistoryService(client, ttl_seconds=60)  # type: ignore[arg-type]
    first = await service.get_history("AAPL260814C00130000")
    second = await service.get_history("AAPL260814C00130000")
    assert first.points[0].close == 1.25
    assert second.contract_symbol == "AAPL260814C00130000"
    assert client.calls == 1
