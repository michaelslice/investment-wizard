from typing import Annotated

from fastapi import APIRouter, Query

from src.options import constants
from src.options.dependencies import OptionChainServiceDep, OptionHistoryServiceDep
from src.options.schemas import OptionChain, OptionHistoryResponse, OptionSearchResponse

router = APIRouter(prefix="/options", tags=["options"])


@router.get("/search", response_model=OptionSearchResponse, response_model_by_alias=True)
async def search_options(
    service: OptionChainServiceDep,
    symbols: str = "AAPL",
    option_type: str | None = None,
    min_dte: int = 0,
    max_dte: int = 365,
    min_moneyness: float | None = None,
    max_moneyness: float | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_iv: float | None = None,
    max_iv: float | None = None,
    min_delta: float | None = None,
    max_delta: float | None = None,
    min_volume: int = 0,
    min_open_interest: int = 0,
    max_spread_percent: float | None = None,
    limit: int = 100,
) -> OptionSearchResponse:
    tickers = [item.strip().upper() for item in symbols.split(",") if item.strip()][:10]
    return await service.search(
        tickers,
        option_type,
        min_dte,
        max_dte,
        min_moneyness,
        max_moneyness,
        min_price,
        max_price,
        min_iv,
        max_iv,
        min_delta,
        max_delta,
        min_volume,
        min_open_interest,
        max_spread_percent,
        min(max(limit, 1), 500),
    )


@router.get("", response_model=OptionChain, response_model_by_alias=True)
async def get_option_chain(
    service: OptionChainServiceDep,
    symbol: Annotated[str, Query(pattern=constants.SYMBOL_PATTERN)] = "AAPL",
    expiration: int | None = None,
) -> OptionChain:
    return await service.get_chain(symbol.upper(), expiration)


@router.get(
    "/history/{contract_symbol}",
    response_model=OptionHistoryResponse,
    response_model_by_alias=True,
)
async def get_option_history(
    contract_symbol: str, service: OptionHistoryServiceDep
) -> OptionHistoryResponse:
    return await service.get_history(contract_symbol)
