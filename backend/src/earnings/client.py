from collections.abc import Iterable
from datetime import UTC, date, datetime, time
from typing import Any

import yfinance as yf


class YahooEarningsClient:
    def get_dates(self, symbol: str) -> list[datetime]:
        calendar = yf.Ticker(symbol).calendar
        if calendar is None or "Earnings Date" not in calendar:
            return []
        raw_dates: Any = calendar["Earnings Date"]
        values: Iterable[Any] = raw_dates if isinstance(raw_dates, list) else [raw_dates]
        dates: list[datetime] = []
        for value in values:
            if isinstance(value, datetime):
                dates.append(value if value.tzinfo else value.replace(tzinfo=UTC))
            elif isinstance(value, date):
                dates.append(datetime.combine(value, time.min, tzinfo=UTC))
        return dates
