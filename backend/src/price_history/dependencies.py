from typing import Annotated

from fastapi import Depends, Request

from src.price_history.service import PriceHistoryService


def get_price_history_service(request: Request) -> PriceHistoryService:
    return request.app.state.price_history_service


PriceHistoryServiceDep = Annotated[PriceHistoryService, Depends(get_price_history_service)]
