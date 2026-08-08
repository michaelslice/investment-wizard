from src.exceptions import AppError


class SectorNotFound(AppError):
    status_code = 404
