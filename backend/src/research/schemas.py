from pydantic import BaseModel, ConfigDict, Field


class SectorSummary(BaseModel):
    slug: str
    label: str
    company_count: int = Field(alias="companyCount")


class CompanyResearch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    name: str
    sector: str
    industry: str
    market_cap: int | None = Field(alias="marketCap")
    current_price: float | None = Field(alias="currentPrice")
    trailing_pe: float | None = Field(alias="trailingPe")
    revenue: int | None
    profit_margin: float | None = Field(alias="profitMargin")
    target_price: float | None = Field(alias="targetPrice")
    recommendation: str | None


class SectorResearch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sector: SectorSummary
    companies: list[CompanyResearch]
    source: str = "Yahoo Finance via yfinance"
