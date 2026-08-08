from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.earnings import constants as earnings_constants
from src.earnings.client import YahooEarningsClient
from src.earnings.router import router as earnings_router
from src.earnings.service import EarningsService
from src.exceptions import register_exception_handlers
from src.options.client import CboeClient
from src.options.router import router as options_router
from src.options.service import OptionChainService


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    async with httpx.AsyncClient(
        base_url=settings.cboe_base_url,
        timeout=settings.request_timeout_seconds,
    ) as client:
        app.state.http_client = client
        app.state.option_chain_service = OptionChainService(
            CboeClient(client, settings), settings.cache_ttl_seconds
        )
        app.state.earnings_service = EarningsService(
            YahooEarningsClient(), earnings_constants.CACHE_TTL_SECONDS
        )
        yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.include_router(options_router, prefix=settings.api_prefix)
    app.include_router(earnings_router, prefix=settings.api_prefix)
    register_exception_handlers(app)
    return app


app = create_app()
