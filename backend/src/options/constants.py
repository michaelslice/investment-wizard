from typing import Final

CBOE_OPTIONS_PATH: Final = "/api/global/delayed_quotes/options/{symbol}.json"
SYMBOL_PATTERN: Final = r"^[A-Z.^-]{1,12}$"
UPSTREAM_HINT: Final = (
    "The upstream market-data endpoint may be rate-limited. Try again shortly."
)
