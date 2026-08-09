from typing import Annotated

from fastapi import Depends, Request

from src.chat.service import ChatService


def get_chat_service(request: Request) -> ChatService:
    return request.app.state.chat_service


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
