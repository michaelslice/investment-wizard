from typing import Annotated, Literal

from fastapi import APIRouter, Query

from src.price_history.dependencies import PriceHistoryServiceDep
from src.price_history.schemas import PriceHistoryResponse

router = APIRouter(prefix="/prices", tags=["price history"])


@router.get("/{symbol}", response_model=PriceHistoryResponse, response_model_by_alias=True)
async def get_price_history(
    symbol: str,
    service: PriceHistoryServiceDep,
    period: Annotated[Literal["6mo", "1y", "3y", "5y", "10y", "max"], Query()] = "1y",
) -> PriceHistoryResponse:
    return await service.get_timeline(symbol.upper(), period)
