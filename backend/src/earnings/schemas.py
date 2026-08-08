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


class HistoricalEarningsReaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    report_date: datetime = Field(alias="reportDate")
    timing: str
    before_session_date: datetime = Field(alias="beforeSessionDate")
    before_close: float = Field(alias="beforeClose")
    next_session_date: datetime = Field(alias="nextSessionDate")
    next_open: float = Field(alias="nextOpen")
    change: float
    change_percent: float = Field(alias="changePercent")
    profit_on_100_shares: float = Field(alias="profitOn100Shares")
    eps_estimate: float | None = Field(None, alias="epsEstimate")
    reported_eps: float | None = Field(None, alias="reportedEps")
    surprise_percent: float | None = Field(None, alias="surprisePercent")


class HistoricalEarningsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    events: list[HistoricalEarningsReaction]
    average_change_percent: float = Field(alias="averageChangePercent")
    positive_reactions: int = Field(alias="positiveReactions")
    source: str = "Yahoo Finance via yfinance"


class EarningsPricePoint(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class EarningsReactionChart(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    before_session_date: datetime = Field(alias="beforeSessionDate")
    next_session_date: datetime = Field(alias="nextSessionDate")
    points: list[EarningsPricePoint]
    trading_days: int = Field(alias="tradingDays")
    interval: str
    source: str = "Yahoo Finance via yfinance"
