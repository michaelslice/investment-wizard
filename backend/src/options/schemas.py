from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PublishedGreeks(BaseModel):
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None
    rho: float | None = None


class OptionContract(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    type: Literal["call", "put"]
    strike: float
    bid: float = 0
    ask: float = 0
    last: float = 0
    change: float = 0
    volume: int = 0
    open_interest: int = Field(0, alias="openInterest")
    implied_volatility: float = Field(0, alias="impliedVolatility")
    in_the_money: bool = Field(False, alias="inTheMoney")
    last_trade: str | None = Field(None, alias="lastTrade")
    previous_close: float | None = Field(None, alias="previousClose")
    published_greeks: PublishedGreeks = Field(alias="publishedGreeks")


class OptionChain(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    spot: float
    spot_change: float = Field(alias="spotChange")
    market_time: int = Field(alias="marketTime")
    currency: str = "USD"
    expirations: list[int]
    selected_expiration: int = Field(alias="selectedExpiration")
    calls: list[OptionContract]
    puts: list[OptionContract]
    source: str
