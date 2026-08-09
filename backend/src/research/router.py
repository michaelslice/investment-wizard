from typing import Annotated

from fastapi import APIRouter, Query

from src.research.dependencies import ResearchServiceDep
from src.research.schemas import CompanyResearch, SectorResearch, SectorSummary, TickerResearch

router = APIRouter(prefix="/research", tags=["market research"])


@router.get("/companies", response_model=list[CompanyResearch], response_model_by_alias=True)
async def get_companies(
    service: ResearchServiceDep,
    symbols: Annotated[str, Query(min_length=1, max_length=300)],
) -> list[CompanyResearch]:
    unique = list(dict.fromkeys(
        symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()
    ))[:50]
    return await service.get_companies(unique)


@router.get("/tickers/{symbol}", response_model=TickerResearch, response_model_by_alias=True)
async def get_ticker_research(symbol: str, service: ResearchServiceDep) -> TickerResearch:
    return await service.get_ticker_research(symbol.upper())


@router.get("/sectors", response_model=list[SectorSummary], response_model_by_alias=True)
async def get_sectors(service: ResearchServiceDep) -> list[SectorSummary]:
    return await service.get_sectors()


@router.get("/sectors/{sector}", response_model=SectorResearch, response_model_by_alias=True)
async def get_sector(
    sector: str,
    service: ResearchServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=50)] = 25,
    query: Annotated[str, Query(max_length=80)] = "",
) -> SectorResearch:
    return await service.get_sector(sector, page, page_size, query.strip())
