from .client import RentCastClient
from .schemas import PropertyListing, PropertySearch, PropertySearchResponse


class RealEstateService:
    def __init__(self, client: RentCastClient) -> None:
        self._client = client

    async def search(self, query: PropertySearch) -> PropertySearchResponse:
        params: dict[str, str | int] = {
            "status": "Active",
            "limit": query.limit,
            "offset": query.offset,
            "includeTotalCount": "true",
        }
        for key, value in (
            ("city", query.city),
            ("state", query.state),
            ("zipCode", query.zip_code),
            ("propertyType", query.property_type),
        ):
            if value:
                params[key] = value
        if query.min_price is not None or query.max_price is not None:
            params["price"] = (
                f"{query.min_price if query.min_price is not None else '*'}:{query.max_price if query.max_price is not None else '*'}"
            )
        if query.min_bedrooms is not None:
            params["bedrooms"] = f"{query.min_bedrooms}:*"
        if query.min_bathrooms is not None:
            params["bathrooms"] = f"{query.min_bathrooms}:*"
        if query.min_square_feet is not None:
            params["squareFootage"] = f"{query.min_square_feet}:*"
        if query.max_days_old is not None:
            params["daysOld"] = f"*:{query.max_days_old}"
        records, total = await self._client.search_sale_listings(params)
        return PropertySearchResponse(
            listings=[self._normalize(item) for item in records],
            total=total,
            limit=query.limit,
            offset=query.offset,
        )

    @staticmethod
    def _normalize(item: dict) -> PropertyListing:
        return PropertyListing(
            id=str(item.get("id", "")),
            address=item.get("formattedAddress")
            or item.get("addressLine1")
            or "Address unavailable",
            city=item.get("city", ""),
            state=item.get("state", ""),
            zip_code=item.get("zipCode"),
            property_type=item.get("propertyType"),
            price=float(item.get("price") or 0),
            bedrooms=item.get("bedrooms"),
            bathrooms=item.get("bathrooms"),
            square_footage=item.get("squareFootage"),
            lot_size=item.get("lotSize"),
            year_built=item.get("yearBuilt"),
            days_on_market=item.get("daysOnMarket"),
            status=item.get("status"),
            latitude=item.get("latitude"),
            longitude=item.get("longitude"),
            listed_date=item.get("listedDate"),
        )
