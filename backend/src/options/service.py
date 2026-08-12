from datetime import UTC, datetime
from time import monotonic, time
from typing import Any

from src.options.client import CboeClient
from src.options.exceptions import OptionChainNotFound
from src.options.schemas import (
    OptionChain,
    OptionContract,
    OptionSearchResponse,
    OptionSearchResult,
    PublishedGreeks,
)
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
        expirations = sorted(
            {details.expiration for _, details in parsed if details.expiration >= cutoff}
        )
        if not expirations:
            raise OptionChainNotFound("No active expirations found")
        selected = expiration if expiration in expirations else expirations[0]
        spot = float(data.get("current_price") or 0)
        contracts = [
            self._map_contract(item, details, spot)
            for item, details in parsed
            if details.expiration == selected
        ]

        timestamp = raw.get("timestamp")
        market_time = (
            int(datetime.fromisoformat(timestamp).replace(tzinfo=UTC).timestamp())
            if timestamp
            else int(time())
        )
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

    async def search(
        self,
        symbols: list[str],
        option_type: str | None,
        min_dte: int,
        max_dte: int,
        min_moneyness: float | None,
        max_moneyness: float | None,
        min_price: float | None,
        max_price: float | None,
        min_iv: float | None,
        max_iv: float | None,
        min_delta: float | None,
        max_delta: float | None,
        min_volume: int,
        min_open_interest: int,
        max_spread_percent: float | None,
        limit: int,
    ) -> OptionSearchResponse:
        now = datetime.now(UTC).date()
        results: list[OptionSearchResult] = []
        scanned = 0
        for symbol in symbols:
            initial = await self.get_chain(symbol, None)
            expirations = [
                value
                for value in initial.expirations
                if min_dte <= (datetime.fromtimestamp(value, UTC).date() - now).days <= max_dte
            ]
            for expiration in expirations:
                chain = (
                    initial
                    if expiration == initial.selected_expiration
                    else await self.get_chain(symbol, expiration)
                )
                contracts = chain.calls + chain.puts
                scanned += len(contracts)
                for contract in contracts:
                    if option_type and contract.type != option_type:
                        continue
                    mark = (
                        (contract.bid + contract.ask) / 2
                        if contract.bid and contract.ask
                        else contract.last
                    )
                    moneyness = (contract.strike / chain.spot - 1) * 100 if chain.spot else 0
                    spread = (contract.ask - contract.bid) / mark * 100 if mark > 0 else 999
                    delta = contract.published_greeks.delta
                    checks = (
                        min_moneyness is None or moneyness >= min_moneyness,
                        max_moneyness is None or moneyness <= max_moneyness,
                        min_price is None or mark >= min_price,
                        max_price is None or mark <= max_price,
                        min_iv is None or contract.implied_volatility >= min_iv,
                        max_iv is None or contract.implied_volatility <= max_iv,
                        min_delta is None or delta is not None and abs(delta) >= min_delta,
                        max_delta is None or delta is not None and abs(delta) <= max_delta,
                        contract.volume >= min_volume,
                        contract.open_interest >= min_open_interest,
                        max_spread_percent is None or spread <= max_spread_percent,
                    )
                    if all(checks):
                        results.append(
                            OptionSearchResult(
                                underlying=chain.symbol,
                                spot=chain.spot,
                                expiration=expiration,
                                dte=(datetime.fromtimestamp(expiration, UTC).date() - now).days,
                                moneyness=moneyness,
                                spreadPercent=spread,
                                contract=contract,
                            )
                        )
        results.sort(key=lambda item: (item.spread_percent, -item.contract.open_interest))
        return OptionSearchResponse(
            results=results[:limit],
            contractsScanned=scanned,
            symbolsScanned=len(symbols),
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
    def _map_contract(
        item: dict[str, Any], details: ParsedOptionSymbol, spot: float
    ) -> OptionContract:
        return OptionContract(
            symbol=item.get("option", ""),
            type=details.option_type,
            strike=details.strike,
            bid=item.get("bid") or 0,
            ask=item.get("ask") or 0,
            last=item.get("last_trade_price") or 0,
            change=item.get("percent_change") or 0,
            volume=item.get("volume") or 0,
            openInterest=item.get("open_interest") or 0,
            impliedVolatility=item.get("iv") or 0,
            inTheMoney=details.strike < spot
            if details.option_type == "call"
            else details.strike > spot,
            lastTrade=item.get("last_trade_time"),
            previousClose=item.get("prev_day_close"),
            publishedGreeks=PublishedGreeks(
                delta=item.get("delta"),
                gamma=item.get("gamma"),
                theta=item.get("theta"),
                vega=item.get("vega"),
                rho=item.get("rho"),
            ),
        )
