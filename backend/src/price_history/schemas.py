from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PricePoint(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class TimelineEarningsEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    earnings_date: datetime = Field(alias="earningsDate")
    eps_estimate: float | None = Field(None, alias="epsEstimate")
    reported_eps: float | None = Field(None, alias="reportedEps")
    surprise_percent: float | None = Field(None, alias="surprisePercent")
    is_upcoming: bool = Field(alias="isUpcoming")


class PriceHistoryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    period: str
    prices: list[PricePoint]
    earnings: list[TimelineEarningsEvent]
    latest_price: float | None = Field(None, alias="latestPrice")
    source: str = "Yahoo Finance via yfinance"
