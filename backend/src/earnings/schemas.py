from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EarningsEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    earnings_date: datetime = Field(alias="earningsDate")
    formatted_date: str = Field(alias="formattedDate")


class EarningsCalendar(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: list[EarningsEvent]
    requested_symbols: int = Field(alias="requestedSymbols")
    matched_symbols: int = Field(alias="matchedSymbols")
    source: str = "Yahoo Finance via yfinance"
