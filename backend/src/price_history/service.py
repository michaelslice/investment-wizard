import asyncio
from time import monotonic

from src.price_history.client import YahooPriceHistoryClient
from src.price_history.schemas import PriceHistoryResponse, PricePoint, TimelineEarningsEvent


class PriceHistoryService:
    def __init__(self, client: YahooPriceHistoryClient, ttl_seconds: int) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._cache: dict[tuple[str, str], tuple[float, PriceHistoryResponse]] = {}

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
