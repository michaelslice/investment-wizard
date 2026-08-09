from typing import Any

import pandas as pd
import yfinance as yf


class YahooOptionHistoryClient:
    def get_history(self, contract_symbol: str) -> list[dict[str, Any]]:
        history = yf.Ticker(contract_symbol).history(
            period="max", interval="1d", auto_adjust=False
        )
        return [
            {
                "date": index.to_pydatetime(),
                "open": self._number(row.get("Open")),
                "high": self._number(row.get("High")),
                "low": self._number(row.get("Low")),
                "close": self._number(row.get("Close")),
                "volume": int(row.get("Volume") or 0),
            }
            for index, row in history.iterrows()
            if not pd.isna(row.get("Close"))
        ]

    @staticmethod
    def _number(value: Any) -> float:
        return 0.0 if value is None or pd.isna(value) else float(value)
