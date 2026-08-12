import re
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class ParsedOptionSymbol:
    expiration: int
    option_type: str
    strike: float


OPTION_PATTERN = re.compile(r"^(.+?)(\d{2})(\d{2})(\d{2})([CP])(\d{8})$")


def parse_option_symbol(value: str) -> ParsedOptionSymbol | None:
    match = OPTION_PATTERN.match(value)
    if not match:
        return None
    _, year, month, day, side, strike = match.groups()
    expiration = datetime(2000 + int(year), int(month), int(day), tzinfo=UTC)
    return ParsedOptionSymbol(
        expiration=int(expiration.timestamp()),
        option_type="call" if side == "C" else "put",
        strike=int(strike) / 1000,
    )
