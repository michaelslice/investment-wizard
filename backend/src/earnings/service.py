import asyncio
from time import monotonic

from src.earnings.client import YahooEarningsClient
from src.earnings.schemas import EarningsCalendar, EarningsEvent


class EarningsService:
    def __init__(self, client: YahooEarningsClient, ttl_seconds: int, concurrency: int = 8) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._semaphore = asyncio.Semaphore(concurrency)
        self._cache: dict[tuple[str, ...], tuple[float, EarningsCalendar]] = {}

    async def get_calendar(self, symbols: tuple[str, ...]) -> EarningsCalendar:
        cached = self._cache.get(symbols)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        results = await asyncio.gather(
            *(self._get_symbol(symbol) for symbol in symbols), return_exceptions=True
        )
        events = sorted(
            (
                event
                for symbol_events in results
                if isinstance(symbol_events, list)
                for event in symbol_events
            ),
            key=lambda event: event.earnings_date,
        )
        calendar = EarningsCalendar(
            events=events,
            requestedSymbols=len(symbols),
            matchedSymbols=len({event.symbol for event in events}),
        )
        self._cache[symbols] = (monotonic(), calendar)
        return calendar

    async def _get_symbol(self, symbol: str) -> list[EarningsEvent]:
        async with self._semaphore:
            dates = await asyncio.to_thread(self._client.get_dates, symbol)
        return [
            EarningsEvent(
                symbol=symbol,
                earningsDate=value,
                formattedDate=value.strftime("%B %d, %Y"),
            )
            for value in dates
        ]
