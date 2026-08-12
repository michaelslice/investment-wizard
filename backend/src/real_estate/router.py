from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

from .schemas import PropertySearch, PropertySearchResponse
from .service import RealEstateService

router = APIRouter(prefix="/real-estate", tags=["real-estate"])


def get_service(request: Request) -> RealEstateService:
    return request.app.state.real_estate_service


@router.get("/listings", response_model=PropertySearchResponse)
async def search_listings(
    query: Annotated[PropertySearch, Depends()],
    service: Annotated[RealEstateService, Depends(get_service)],
) -> PropertySearchResponse:
    try:
        return await service.search(query)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except httpx.HTTPStatusError as error:
        status = 429 if error.response.status_code == 429 else 502
        raise HTTPException(
            status_code=status,
            detail="The property-data provider rejected the request. Check the API key or try again shortly.",
        ) from error
