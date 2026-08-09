from typing import Annotated

import httpx
from fastapi import Depends, Request

from src.config import Settings, get_settings
from src.options.client import CboeClient
from src.options.history_service import OptionHistoryService
from src.options.service import OptionChainService


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_cboe_client(
    http_client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> CboeClient:
    return CboeClient(http_client, settings)


CboeClientDep = Annotated[CboeClient, Depends(get_cboe_client)]


def get_option_chain_service(request: Request) -> OptionChainService:
    return request.app.state.option_chain_service


OptionChainServiceDep = Annotated[OptionChainService, Depends(get_option_chain_service)]


def get_option_history_service(request: Request) -> OptionHistoryService:
    return request.app.state.option_history_service


OptionHistoryServiceDep = Annotated[OptionHistoryService, Depends(get_option_history_service)]
