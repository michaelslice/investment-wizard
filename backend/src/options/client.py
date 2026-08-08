from typing import Any

import httpx

from src.config import Settings
from src.options import constants
from src.options.exceptions import MarketDataUnavailable


class CboeClient:
    def __init__(self, http_client: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http_client
        self._settings = settings

    async def get_chain(self, symbol: str) -> dict[str, Any]:
        try:
            response = await self._http.get(
                constants.CBOE_OPTIONS_PATH.format(symbol=symbol),
                headers={"User-Agent": "optionscope/1.0", "Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise MarketDataUnavailable(
                "Market data provider request failed", hint=constants.UPSTREAM_HINT
            ) from error
