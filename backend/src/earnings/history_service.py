import asyncio
from datetime import UTC, date, datetime, time
from time import monotonic

from src.earnings.history_client import YahooEarningsHistoryClient
from src.earnings.schemas import (
    EarningsPricePoint,
    EarningsReactionChart,
    HistoricalEarningsReaction,
    HistoricalEarningsResponse,
)


class EarningsHistoryService:
    def __init__(self, client: YahooEarningsHistoryClient, ttl_seconds: int) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._cache: dict[tuple[str, int], tuple[float, HistoricalEarningsResponse]] = {}
        self._chart_cache: dict[
            tuple[str, date, date, int], tuple[float, EarningsReactionChart]
        ] = {}

    async def get_history(self, symbol: str, limit: int) -> HistoricalEarningsResponse:
        key = (symbol, limit)
        cached = self._cache.get(key)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        raw = await asyncio.to_thread(self._client.get_history, symbol, limit)
        events = [HistoricalEarningsReaction.model_validate(item) for item in raw]
        response = HistoricalEarningsResponse(
            symbol=symbol,
            events=events,
            averageChangePercent=sum(event.change_percent for event in events) / len(events)
            if events
            else 0,
            positiveReactions=sum(event.change > 0 for event in events),
        )
        self._cache[key] = (monotonic(), response)
        return response

    async def get_reaction_chart(
        self, symbol: str, before_session: date, next_session: date, trading_days: int
    ) -> EarningsReactionChart:
        key = (symbol, before_session, next_session, trading_days)
        cached = self._chart_cache.get(key)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        raw = await asyncio.to_thread(
            self._client.get_reaction_chart,
            symbol,
            before_session,
            next_session,
            trading_days,
        )
        response = EarningsReactionChart(
            symbol=symbol,
            beforeSessionDate=datetime.combine(before_session, time.min, tzinfo=UTC),
            nextSessionDate=datetime.combine(next_session, time.min, tzinfo=UTC),
            points=[EarningsPricePoint.model_validate(item) for item in raw],
            tradingDays=trading_days,
            interval="Hourly" if trading_days <= 14 else "Daily",
        )
        self._chart_cache[key] = (monotonic(), response)
        return response
