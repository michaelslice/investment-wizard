import os
from typing import Any

import httpx


class InvestmentWizardApiClient:
    """Async client for the local investment-wizard FastAPI application."""

    def __init__(self, base_url: str | None = None, timeout_seconds: float = 30) -> None:
        self._base_url = (
            base_url
            or os.getenv("INVESTMENT_WIZARD_API_URL")
            or os.getenv("OPTIONSCOPE_API_URL")
            or "http://127.0.0.1:8000/api"
        ).rstrip("/")
        self._timeout = timeout_seconds

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        async with httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            follow_redirects=True,
        ) as client:
            response = await client.get(path, params=params)
            response.raise_for_status()
            return response.json()
