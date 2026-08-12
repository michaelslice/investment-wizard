from typing import Annotated

from fastapi import Depends, Request

from src.earnings.history_service import EarningsHistoryService
from src.earnings.service import EarningsService


def get_earnings_service(request: Request) -> EarningsService:
    return request.app.state.earnings_service


EarningsServiceDep = Annotated[EarningsService, Depends(get_earnings_service)]


def get_earnings_history_service(request: Request) -> EarningsHistoryService:
    return request.app.state.earnings_history_service


EarningsHistoryServiceDep = Annotated[EarningsHistoryService, Depends(get_earnings_history_service)]
