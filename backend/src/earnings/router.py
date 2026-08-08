from typing import Annotated

from fastapi import APIRouter, Query

from src.earnings import constants
from src.earnings.dependencies import EarningsServiceDep
from src.earnings.schemas import EarningsCalendar

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
