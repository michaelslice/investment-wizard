from datetime import UTC, datetime
from time import monotonic, time
from typing import Any

from src.options.client import CboeClient
from src.options.exceptions import OptionChainNotFound
from src.options.schemas import OptionChain, OptionContract, PublishedGreeks
from src.options.utils import ParsedOptionSymbol, parse_option_symbol


class OptionChainService:
    def __init__(self, client: CboeClient, ttl_seconds: int = 30) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._cache: dict[str, tuple[float, dict[str, Any]]] = {}

    async def get_chain(self, symbol: str, expiration: int | None) -> OptionChain:
        raw = await self._get_cached(symbol)
        data = raw.get("data") or {}
        raw_options = data.get("options") or []
        if not raw_options:
            raise OptionChainNotFound("No option chain found")

        parsed: list[tuple[dict[str, Any], ParsedOptionSymbol]] = []
        for item in raw_options:
            details = parse_option_symbol(item.get("option", ""))
            if details:
                parsed.append((item, details))

        cutoff = int(time()) - 86_400
        expirations = sorted({details.expiration for _, details in parsed if details.expiration >= cutoff})
        if not expirations:
            raise OptionChainNotFound("No active expirations found")
        selected = expiration if expiration in expirations else expirations[0]
        spot = float(data.get("current_price") or 0)
        contracts = [self._map_contract(item, details, spot) for item, details in parsed if details.expiration == selected]

        timestamp = raw.get("timestamp")
        market_time = int(datetime.fromisoformat(timestamp).replace(tzinfo=UTC).timestamp()) if timestamp else int(time())
        return OptionChain(
            symbol=data.get("symbol") or symbol,
            spot=spot,
            spotChange=float(data.get("price_change_percent") or 0),
            marketTime=market_time,
            expirations=expirations,
            selectedExpiration=selected,
            calls=[contract for contract in contracts if contract.type == "call"],
            puts=[contract for contract in contracts if contract.type == "put"],
            source="Cboe delayed quotes",
        )

    async def _get_cached(self, symbol: str) -> dict[str, Any]:
        cached = self._cache.get(symbol)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        value = await self._client.get_chain(symbol)
        self._cache[symbol] = (monotonic(), value)
        return value

    @staticmethod
    def _map_contract(item: dict[str, Any], details: ParsedOptionSymbol, spot: float) -> OptionContract:
        return OptionContract(
            symbol=item.get("option", ""), type=details.option_type, strike=details.strike,
            bid=item.get("bid") or 0, ask=item.get("ask") or 0,
            last=item.get("last_trade_price") or 0, change=item.get("percent_change") or 0,
            volume=item.get("volume") or 0, openInterest=item.get("open_interest") or 0,
            impliedVolatility=item.get("iv") or 0,
            inTheMoney=details.strike < spot if details.option_type == "call" else details.strike > spot,
            lastTrade=item.get("last_trade_time"), previousClose=item.get("prev_day_close"),
            publishedGreeks=PublishedGreeks(
                delta=item.get("delta"), gamma=item.get("gamma"), theta=item.get("theta"),
                vega=item.get("vega"), rho=item.get("rho"),
            ),
        )
