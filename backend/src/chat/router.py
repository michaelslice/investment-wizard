from fastapi import APIRouter

from src.chat.dependencies import ChatServiceDep
from src.chat.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, response_model_by_alias=True)
async def chat(request: ChatRequest, service: ChatServiceDep) -> ChatResponse:
    return await service.respond(request.messages)
