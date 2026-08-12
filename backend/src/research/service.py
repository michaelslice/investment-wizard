import asyncio
from time import monotonic

from src.research import constants
from src.research.client import YahooResearchClient
from src.research.exceptions import SectorNotFound
from src.research.schemas import (
    CompanyResearch,
    HoldersResponse,
    InstitutionalHolder,
    SectorResearch,
    SectorSummary,
    TickerResearch,
)


class ResearchService:
    def __init__(self, client: YahooResearchClient, ttl_seconds: int, concurrency: int = 6) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._semaphore = asyncio.Semaphore(concurrency)
        self._cache: dict[tuple[str, int, int, str], tuple[float, SectorResearch]] = {}
        self._universe_cache: tuple[float, list[dict[str, str]]] | None = None
        self._ticker_cache: dict[str, tuple[float, TickerResearch]] = {}
        self._holders_cache: dict[str, tuple[float, HoldersResponse]] = {}

    async def get_sectors(self) -> list[SectorSummary]:
        universe = await self._get_universe()
        counts = {slug: 0 for slug in constants.GICS_TO_SLUG.values()}
        for company in universe:
            slug = constants.GICS_TO_SLUG.get(company["sector"])
            if slug:
                counts[slug] += 1
        return [SectorSummary(slug="all", label="S&P 500", companyCount=len(universe))] + [
            SectorSummary(slug=slug, label=constants.SECTOR_LABELS[slug], companyCount=count)
            for slug, count in counts.items()
        ]

    async def get_sector(
        self, slug: str, page: int = 1, page_size: int = 25, query: str = ""
    ) -> SectorResearch:
        if slug != "all" and slug not in constants.GICS_TO_SLUG.values():
            raise SectorNotFound(f"Unknown sector: {slug}")
        key = (slug, page, page_size, query.upper())
        cached = self._cache.get(key)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        universe = await self._get_universe()
        selected = [
            company
            for company in universe
            if (slug == "all" or constants.GICS_TO_SLUG.get(company["sector"]) == slug)
            and (
                not query
                or query.upper() in company["symbol"].upper()
                or query.lower() in company["name"].lower()
            )
        ]
        total = len(selected)
        start = (page - 1) * page_size
        page_companies = selected[start : start + page_size]
        results = await asyncio.gather(
            *(self._get_company(company) for company in page_companies), return_exceptions=True
        )
        companies = sorted(
            (result for result in results if isinstance(result, CompanyResearch)),
            key=lambda company: company.market_cap or 0,
            reverse=True,
        )
        response = SectorResearch(
            sector=SectorSummary(
                slug=slug,
                label=constants.SECTOR_LABELS[slug],
                companyCount=total,
            ),
            companies=companies,
            totalCount=total,
            page=page,
            pageSize=page_size,
        )
        self._cache[key] = (monotonic(), response)
        return response

    async def get_companies(self, symbols: list[str]) -> list[CompanyResearch]:
        results = await asyncio.gather(
            *(
                self._get_company(
                    {
                        "symbol": symbol,
                        "name": symbol,
                        "sector": "N/A",
                        "industry": "N/A",
                    }
                )
                for symbol in symbols
            ),
            return_exceptions=True,
        )
        return [result for result in results if isinstance(result, CompanyResearch)]

    async def get_ticker_research(self, symbol: str) -> TickerResearch:
        cached = self._ticker_cache.get(symbol)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        async with self._semaphore:
            raw = await asyncio.to_thread(self._client.get_ticker_research, symbol)
        response = TickerResearch.model_validate(raw)
        self._ticker_cache[symbol] = (monotonic(), response)
        return response

    async def get_holders(self, symbol: str) -> HoldersResponse:
        cached = self._holders_cache.get(symbol)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        async with self._semaphore:
            raw = await asyncio.to_thread(self._client.get_holders, symbol)
        response = HoldersResponse(
            symbol=symbol,
            holders=[InstitutionalHolder.model_validate(item) for item in raw],
        )
        self._holders_cache[symbol] = (monotonic(), response)
        return response

    async def _get_company(self, constituent: dict[str, str]) -> CompanyResearch:
        async with self._semaphore:
            value = await asyncio.to_thread(self._client.get_company, constituent["symbol"])
        if constituent["name"] != constituent["symbol"]:
            value["name"] = constituent["name"]
        if constituent["sector"] != "N/A":
            value["sector"] = constituent["sector"]
        if constituent["industry"] != "N/A":
            value["industry"] = constituent["industry"]
        return CompanyResearch.model_validate(value)

    async def _get_universe(self) -> list[dict[str, str]]:
        if self._universe_cache and monotonic() - self._universe_cache[0] < 86_400:
            return self._universe_cache[1]
        universe = await asyncio.to_thread(self._client.get_constituents)
        self._universe_cache = (monotonic(), universe)
        return universe
