from typing import Any

import httpx


class RentCastClient:
    def __init__(self, api_key: str | None) -> None:
        self._api_key = api_key

    async def search_sale_listings(self, params: dict[str, Any]) -> tuple[list[dict], int]:
        if not self._api_key:
            raise RuntimeError(
                "Real-estate data is not configured. Add RENTCAST_API_KEY to backend/.env."
            )
        async with httpx.AsyncClient(
            base_url="https://api.rentcast.io/v1",
            timeout=15,
            headers={"X-Api-Key": self._api_key, "Accept": "application/json"},
        ) as client:
            response = await client.get("/listings/sale", params=params)
            response.raise_for_status()
            records = response.json()
            return records, int(response.headers.get("X-Total-Count", len(records)))
