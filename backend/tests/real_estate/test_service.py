from unittest.mock import AsyncMock

import pytest

from src.real_estate.schemas import PropertySearch
from src.real_estate.service import RealEstateService


@pytest.mark.asyncio
async def test_search_builds_provider_ranges_and_normalizes_listing() -> None:
    client = AsyncMock()
    client.search_sale_listings.return_value = (
        [
            {
                "id": "one",
                "formattedAddress": "1 Main St, Austin, TX 78701",
                "city": "Austin",
                "state": "TX",
                "price": 500000,
                "squareFootage": 2000,
            }
        ],
        1,
    )
    result = await RealEstateService(client).search(
        PropertySearch(
            city="Austin", state="TX", min_price=250000, max_price=600000, min_bedrooms=2
        )
    )
    params = client.search_sale_listings.await_args.args[0]
    assert params["price"] == "250000:600000"
    assert params["bedrooms"] == "2.0:*"
    assert result.listings[0].price == 500000
    assert result.total == 1
