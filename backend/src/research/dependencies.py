from typing import Annotated

from fastapi import Depends, Request

from src.research.service import ResearchService


def get_research_service(request: Request) -> ResearchService:
    return request.app.state.research_service


ResearchServiceDep = Annotated[ResearchService, Depends(get_research_service)]
