from typing import Annotated

from fastapi import APIRouter, Query

from src.options import constants
from src.options.dependencies import OptionChainServiceDep, OptionHistoryServiceDep
from src.options.schemas import OptionChain, OptionHistoryResponse

router = APIRouter(prefix="/options", tags=["options"])


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
