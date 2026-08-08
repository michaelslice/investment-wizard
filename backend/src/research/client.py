from typing import Any

import yfinance as yf


class YahooResearchClient:
    def get_company(self, symbol: str) -> dict[str, Any]:
        info = yf.Ticker(symbol).info
        return {
            "symbol": symbol,
            "name": info.get("longName") or info.get("shortName") or symbol,
            "sector": info.get("sector") or "N/A",
            "industry": info.get("industry") or "N/A",
            "marketCap": info.get("marketCap"),
            "currentPrice": info.get("currentPrice") or info.get("regularMarketPrice"),
            "trailingPe": info.get("trailingPE"),
            "revenue": info.get("totalRevenue"),
            "profitMargin": info.get("profitMargins"),
            "targetPrice": info.get("targetMeanPrice"),
            "recommendation": info.get("recommendationKey"),
        }
