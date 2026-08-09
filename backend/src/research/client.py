import csv
from io import StringIO
from math import isnan
from typing import Any

import httpx
import yfinance as yf

from src.research import constants


class YahooResearchClient:
    def get_constituents(self) -> list[dict[str, str]]:
        response = httpx.get(
            constants.CONSTITUENTS_URL,
            headers={"User-Agent": "investment-wizard/1.0"},
            follow_redirects=True,
            timeout=15,
        )
        response.raise_for_status()
        return [
            {
                "symbol": row["Symbol"].replace(".", "-"),
                "name": row["Security"],
                "sector": row["GICS Sector"],
                "industry": row["GICS Sub-Industry"],
            }
            for row in csv.DictReader(StringIO(response.text))
        ]

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

    def get_ticker_research(self, symbol: str) -> dict[str, Any]:
        info = yf.Ticker(symbol).info
        return {
            "symbol": symbol,
            "name": info.get("longName") or info.get("shortName") or symbol,
            "description": info.get("longBusinessSummary"),
            "sector": info.get("sector"), "industry": info.get("industry"),
            "website": info.get("website"), "country": info.get("country"),
            "employees": info.get("fullTimeEmployees"), "currency": info.get("currency") or "USD",
            "currentPrice": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previousClose": info.get("previousClose"), "marketCap": info.get("marketCap"),
            "enterpriseValue": info.get("enterpriseValue"), "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"), "beta": info.get("beta"),
            "trailingPe": info.get("trailingPE"), "forwardPe": info.get("forwardPE"),
            "pegRatio": info.get("trailingPegRatio") or info.get("pegRatio"),
            "priceToSales": info.get("priceToSalesTrailing12Months"), "priceToBook": info.get("priceToBook"),
            "enterpriseToRevenue": info.get("enterpriseToRevenue"), "enterpriseToEbitda": info.get("enterpriseToEbitda"),
            "revenue": info.get("totalRevenue"), "revenueGrowth": info.get("revenueGrowth"),
            "grossProfit": info.get("grossProfits"), "ebitda": info.get("ebitda"),
            "netIncome": info.get("netIncomeToCommon"), "earningsGrowth": info.get("earningsGrowth"),
            "dilutedEps": info.get("trailingEps"), "grossMargin": info.get("grossMargins"),
            "operatingMargin": info.get("operatingMargins"), "profitMargin": info.get("profitMargins"),
            "returnOnAssets": info.get("returnOnAssets"), "returnOnEquity": info.get("returnOnEquity"),
            "totalCash": info.get("totalCash"), "totalDebt": info.get("totalDebt"),
            "debtToEquity": info.get("debtToEquity"), "currentRatio": info.get("currentRatio"),
            "quickRatio": info.get("quickRatio"), "operatingCashFlow": info.get("operatingCashflow"),
            "freeCashFlow": info.get("freeCashflow"),
            "dividendYield": self._yield_fraction(info.get("dividendYield")),
            "payoutRatio": info.get("payoutRatio"), "sharesOutstanding": info.get("sharesOutstanding"),
            "floatShares": info.get("floatShares"), "sharesShort": info.get("sharesShort"),
            "shortRatio": info.get("shortRatio"), "heldByInsiders": info.get("heldPercentInsiders"),
            "heldByInstitutions": info.get("heldPercentInstitutions"),
            "targetLow": info.get("targetLowPrice"), "targetMean": info.get("targetMeanPrice"),
            "targetHigh": info.get("targetHighPrice"), "recommendation": info.get("recommendationKey"),
            "analystOpinions": info.get("numberOfAnalystOpinions"),
        }

    def get_holders(self, symbol: str) -> list[dict[str, Any]]:
        frame = yf.Ticker(symbol).institutional_holders
        if frame is None or frame.empty:
            return []
        holders: list[dict[str, Any]] = []
        for _, row in frame.iterrows():
            values = {str(key).lower().replace(" ", "").replace("%", "pct"): value for key, value in row.items()}
            name = values.get("holder") or values.get("organization")
            shares = values.get("shares") or values.get("position")
            if not name or shares is None:
                continue
            percent = self._optional_number(values.get("pctout") or values.get("pctheld"))
            change = self._optional_number(values.get("pctchange") or values.get("change"))
            reported = values.get("datereported") or values.get("reportdate")
            holders.append({
                "name": str(name),
                "shares": int(shares),
                "value": self._optional_int(values.get("value")),
                "percentHeld": percent * 100 if percent is not None and abs(percent) <= 1 else percent,
                "changePercent": change * 100 if change is not None and abs(change) <= 1 else change,
                "reportedDate": reported.isoformat() if hasattr(reported, "isoformat") else None,
            })
        return sorted(holders, key=lambda item: item["shares"], reverse=True)

    @staticmethod
    def _yield_fraction(value: Any) -> float | None:
        if value is None:
            return None
        numeric = float(value)
        return numeric / 100 if numeric > 0.1 else numeric

    @staticmethod
    def _optional_number(value: Any) -> float | None:
        if value is None or bool(getattr(value, "isna", lambda: False)()):
            return None
        try:
            numeric = float(value)
            return None if isnan(numeric) else numeric
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _optional_int(value: Any) -> int | None:
        number = YahooResearchClient._optional_number(value)
        return int(number) if number is not None else None
