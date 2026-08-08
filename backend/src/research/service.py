import asyncio
from time import monotonic

from src.research import constants
from src.research.client import YahooResearchClient
from src.research.exceptions import SectorNotFound
from src.research.schemas import CompanyResearch, SectorResearch, SectorSummary


class ResearchService:
    def __init__(self, client: YahooResearchClient, ttl_seconds: int, concurrency: int = 6) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._semaphore = asyncio.Semaphore(concurrency)
        self._cache: dict[str, tuple[float, SectorResearch]] = {}

    def get_sectors(self) -> list[SectorSummary]:
        return [
            SectorSummary(slug=slug, label=constants.SECTOR_LABELS[slug], companyCount=len(symbols))
            for slug, symbols in constants.SECTOR_SYMBOLS.items()
        ]

    async def get_sector(self, slug: str) -> SectorResearch:
        symbols = constants.SECTOR_SYMBOLS.get(slug)
        if symbols is None:
            raise SectorNotFound(f"Unknown sector: {slug}")
        cached = self._cache.get(slug)
        if cached and monotonic() - cached[0] < self._ttl:
            return cached[1]
        results = await asyncio.gather(
            *(self._get_company(symbol) for symbol in symbols), return_exceptions=True
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
                companyCount=len(companies),
            ),
            companies=companies,
        )
        self._cache[slug] = (monotonic(), response)
        return response

    async def _get_company(self, symbol: str) -> CompanyResearch:
        async with self._semaphore:
            value = await asyncio.to_thread(self._client.get_company, symbol)
        return CompanyResearch.model_validate(value)
