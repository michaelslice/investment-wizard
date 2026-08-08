from src.exceptions import AppError


class OptionChainNotFound(AppError):
    status_code = 404


class MarketDataUnavailable(AppError):
    status_code = 502
