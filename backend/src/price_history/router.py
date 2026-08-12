from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Query

from src.price_history.dependencies import PriceHistoryServiceDep
from src.price_history.schemas import IntradaySessionResponse, PriceHistoryResponse

router = APIRouter(prefix="/prices", tags=["price history"])


@router.get("/{symbol}", response_model=PriceHistoryResponse, response_model_by_alias=True)
async def get_price_history(
    symbol: str,
    service: PriceHistoryServiceDep,
    period: Annotated[Literal["1mo", "3mo", "6mo", "1y", "3y", "5y", "10y", "max"], Query()] = "1y",
) -> PriceHistoryResponse:
    return await service.get_timeline(symbol.upper(), period)


@router.get(
    "/{symbol}/intraday",
    response_model=IntradaySessionResponse,
    response_model_by_alias=True,
)
async def get_intraday_session(
    symbol: str,
    session_date: date,
    service: PriceHistoryServiceDep,
) -> IntradaySessionResponse:
    return await service.get_intraday_session(symbol.upper(), session_date)
