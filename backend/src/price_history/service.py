import asyncio
from datetime import date
from time import monotonic

from src.price_history.client import YahooPriceHistoryClient
from src.price_history.schemas import (
    IntradayPricePoint,
    IntradaySessionResponse,
    PriceHistoryResponse,
    PricePoint,
    TimelineEarningsEvent,
)


class PriceHistoryService:
    def __init__(self, client: YahooPriceHistoryClient, ttl_seconds: int) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._cache: dict[tuple[str, str], tuple[float, PriceHistoryResponse]] = {}
        self._intraday_cache: dict[tuple[str, date], tuple[float, IntradaySessionResponse]] = {}

    async def get_timeline(self, symbol: str, period: str) -> PriceHistoryResponse:
        key = (symbol, period)
        cached = self._cache.get(key)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        raw = await asyncio.to_thread(self._client.get_timeline, symbol, period)
        prices = [PricePoint.model_validate(item) for item in raw["prices"]]
        response = PriceHistoryResponse(
            symbol=symbol,
            period=period,
            prices=prices,
            earnings=[TimelineEarningsEvent.model_validate(item) for item in raw["earnings"]],
            latestPrice=prices[-1].close if prices else None,
        )
        self._cache[key] = (monotonic(), response)
        return response

    async def get_intraday_session(
        self, symbol: str, session_date: date
    ) -> IntradaySessionResponse:
        key = (symbol, session_date)
        cached = self._intraday_cache.get(key)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        raw = await asyncio.to_thread(self._client.get_intraday_session, symbol, session_date)
        response = IntradaySessionResponse(
            symbol=symbol,
            sessionDate=session_date.isoformat(),
            points=[IntradayPricePoint.model_validate(item) for item in raw],
        )
        self._intraday_cache[key] = (monotonic(), response)
        return response
