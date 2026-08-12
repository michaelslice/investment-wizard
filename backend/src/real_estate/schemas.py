from pydantic import BaseModel, Field


class PropertyListing(BaseModel):
    id: str
    address: str
    city: str
    state: str
    zip_code: str | None = None
    property_type: str | None = None
    price: float
    bedrooms: float | None = None
    bathrooms: float | None = None
    square_footage: float | None = None
    lot_size: float | None = None
    year_built: int | None = None
    days_on_market: int | None = None
    status: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    listed_date: str | None = None


class PropertySearchResponse(BaseModel):
    listings: list[PropertyListing]
    total: int
    limit: int
    offset: int
    provider: str = "RentCast"


class PropertySearch(BaseModel):
    city: str | None = None
    state: str | None = Field(default=None, min_length=2, max_length=2)
    zip_code: str | None = None
    property_type: str | None = None
    min_price: int | None = Field(default=None, ge=0)
    max_price: int | None = Field(default=None, ge=0)
    min_bedrooms: float | None = Field(default=None, ge=0)
    min_bathrooms: float | None = Field(default=None, ge=0)
    min_square_feet: int | None = Field(default=None, ge=0)
    max_days_old: int | None = Field(default=None, ge=1)
    limit: int = Field(default=25, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
