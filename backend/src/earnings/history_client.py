from datetime import date, timedelta
from math import isnan
from typing import Any

import pandas as pd
import yfinance as yf


class YahooEarningsHistoryClient:
    def get_history(self, symbol: str, limit: int) -> list[dict[str, Any]]:
        ticker = yf.Ticker(symbol)
        earnings = ticker.get_earnings_dates(limit=max(limit + 2, 12))
        if earnings is None or earnings.empty:
            return []
        earnings = (
            earnings[earnings["Reported EPS"].notna()].sort_index(ascending=False).head(limit)
        )
        if earnings.empty:
            return []
        start = earnings.index.min().date() - timedelta(days=10)
        end = earnings.index.max().date() + timedelta(days=10)
        prices = ticker.history(start=start, end=end, auto_adjust=False)
        if prices.empty:
            return []

        sessions = [(index.date(), index.to_pydatetime(), row) for index, row in prices.iterrows()]
        records: list[dict[str, Any]] = []
        for report_date, row in earnings.iterrows():
            report = report_date.to_pydatetime()
            after_close = report.hour >= 16
            prior = (
                [session for session in sessions if session[0] <= report.date()]
                if after_close
                else [session for session in sessions if session[0] < report.date()]
            )
            following = (
                [session for session in sessions if session[0] > report.date()]
                if after_close
                else [session for session in sessions if session[0] >= report.date()]
            )
            if not prior or not following:
                continue
            before, after = prior[-1], following[0]
            before_close, next_open = float(before[2]["Close"]), float(after[2]["Open"])
            change = next_open - before_close
            records.append(
                {
                    "reportDate": report,
                    "timing": "After market close" if after_close else "Before market open",
                    "beforeSessionDate": before[1],
                    "beforeClose": before_close,
                    "nextSessionDate": after[1],
                    "nextOpen": next_open,
                    "change": change,
                    "changePercent": change / before_close * 100,
                    "profitOn100Shares": change * 100,
                    "epsEstimate": self._number(row.get("EPS Estimate")),
                    "reportedEps": self._number(row.get("Reported EPS")),
                    "surprisePercent": self._number(row.get("Surprise(%)")),
                }
            )
        return records

    def get_reaction_chart(
        self, symbol: str, before_session: date, next_session: date, trading_days: int
    ) -> list[dict[str, Any]]:
        calendar_padding = max(5, int(trading_days * 1.6) + 10)
        interval = "60m" if trading_days <= 14 else "1d"
        prices = yf.Ticker(symbol).history(
            start=before_session - timedelta(days=calendar_padding),
            end=next_session + timedelta(days=calendar_padding),
            interval=interval,
            auto_adjust=False,
            prepost=False,
        )
        if prices.empty:
            return []
        available_dates = sorted({index.date() for index in prices.index})
        before_dates = [value for value in available_dates if value <= before_session][
            -trading_days:
        ]
        after_dates = [value for value in available_dates if value >= next_session][:trading_days]
        selected_dates = set(before_dates + after_dates)
        return [
            {
                "timestamp": index.to_pydatetime(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }
            for index, row in prices.iterrows()
            if index.date() in selected_dates
        ]

    @staticmethod
    def _number(value: Any) -> float | None:
        if value is None or pd.isna(value) or (isinstance(value, float) and isnan(value)):
            return None
        return float(value)
