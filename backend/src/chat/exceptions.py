from src.exceptions import AppError


class ChatUnavailable(AppError):
    status_code = 503
