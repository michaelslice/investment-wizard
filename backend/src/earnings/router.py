from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query

from src.earnings import constants
from src.earnings.dependencies import EarningsHistoryServiceDep, EarningsServiceDep
from src.earnings.schemas import (
    EarningsCalendar,
    EarningsReactionChart,
    HistoricalEarningsResponse,
)

router = APIRouter(prefix="/earnings", tags=["earnings"])


@router.get("", response_model=EarningsCalendar, response_model_by_alias=True)
async def get_upcoming_earnings(
    service: EarningsServiceDep,
    symbols: Annotated[str | None, Query(description="Comma-separated ticker symbols")] = None,
) -> EarningsCalendar:
    selected = constants.DEFAULT_SYMBOLS
    if symbols:
        selected = tuple(
            dict.fromkeys(
                symbol.strip().upper()
                for symbol in symbols.split(",")
                if symbol.strip() and symbol.strip().replace("-", "").isalnum()
            )
        )[: constants.MAX_SYMBOLS]
    return await service.get_calendar(selected)


@router.get(
    "/history/{symbol}",
    response_model=HistoricalEarningsResponse,
    response_model_by_alias=True,
)
async def get_historical_earnings(
    symbol: str,
    service: EarningsHistoryServiceDep,
    limit: Annotated[int, Query(ge=1, le=24)] = 12,
) -> HistoricalEarningsResponse:
    return await service.get_history(symbol.upper(), limit)


@router.get(
    "/history/{symbol}/chart",
    response_model=EarningsReactionChart,
    response_model_by_alias=True,
)
async def get_earnings_reaction_chart(
    symbol: str,
    service: EarningsHistoryServiceDep,
    before_session: date,
    next_session: date,
    trading_days: Annotated[int, Query(ge=1, le=252)] = 1,
) -> EarningsReactionChart:
    return await service.get_reaction_chart(
        symbol.upper(), before_session, next_session, trading_days
    )
