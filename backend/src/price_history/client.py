from datetime import UTC, datetime
from math import isnan
from typing import Any

import pandas as pd
import yfinance as yf


class YahooPriceHistoryClient:
    def get_timeline(self, symbol: str, period: str) -> dict[str, Any]:
        ticker = yf.Ticker(symbol)
        prices = ticker.history(period=period, interval="1d", auto_adjust=True)
        earnings = ticker.get_earnings_dates(limit=100)
        price_points = [
            {
                "date": index.to_pydatetime(), "open": float(row["Open"]),
                "high": float(row["High"]), "low": float(row["Low"]),
                "close": float(row["Close"]), "volume": int(row["Volume"]),
            }
            for index, row in prices.iterrows()
        ]
        now = datetime.now(UTC)
        events: list[dict[str, Any]] = []
        if earnings is not None:
            for date, row in earnings.sort_index().iterrows():
                value = date.to_pydatetime()
                normalized = value if value.tzinfo else value.replace(tzinfo=UTC)
                events.append({
                    "earningsDate": normalized,
                    "epsEstimate": self._number(row.get("EPS Estimate")),
                    "reportedEps": self._number(row.get("Reported EPS")),
                    "surprisePercent": self._number(row.get("Surprise(%)")),
                    "isUpcoming": normalized.astimezone(UTC) > now,
                })
        return {"prices": price_points, "earnings": events}

    @staticmethod
    def _number(value: Any) -> float | None:
        if value is None or pd.isna(value) or (isinstance(value, float) and isnan(value)):
            return None
        return float(value)
