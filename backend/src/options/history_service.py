import asyncio
from time import monotonic

from src.options.exceptions import OptionChainNotFound
from src.options.history_client import YahooOptionHistoryClient
from src.options.schemas import OptionHistoryPoint, OptionHistoryResponse
from src.options.utils import parse_option_symbol


class OptionHistoryService:
    def __init__(self, client: YahooOptionHistoryClient, ttl_seconds: int = 900) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._cache: dict[str, tuple[float, OptionHistoryResponse]] = {}

    async def get_history(self, contract_symbol: str) -> OptionHistoryResponse:
        symbol = contract_symbol.upper()
        if parse_option_symbol(symbol) is None:
            raise OptionChainNotFound("Invalid option contract symbol")
        cached = self._cache.get(symbol)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        raw = await asyncio.to_thread(self._client.get_history, symbol)
        points = [OptionHistoryPoint.model_validate(item) for item in raw]
        if not points:
            raise OptionChainNotFound("No historical prices found for this contract")
        response = OptionHistoryResponse(contractSymbol=symbol, points=points)
        self._cache[symbol] = (monotonic(), response)
        return response
