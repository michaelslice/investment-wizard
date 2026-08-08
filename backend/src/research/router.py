from fastapi import APIRouter

from src.research.dependencies import ResearchServiceDep
from src.research.schemas import SectorResearch, SectorSummary

router = APIRouter(prefix="/research", tags=["market research"])


@router.get("/sectors", response_model=list[SectorSummary], response_model_by_alias=True)
async def get_sectors(service: ResearchServiceDep) -> list[SectorSummary]:
    return service.get_sectors()


@router.get("/sectors/{sector}", response_model=SectorResearch, response_model_by_alias=True)
async def get_sector(sector: str, service: ResearchServiceDep) -> SectorResearch:
    return await service.get_sector(sector)
