SECTOR_SYMBOLS: dict[str, tuple[str, ...]] = {
    "technology": ("NVDA", "AAPL", "MSFT", "AVGO", "ORCL", "CRM", "AMD", "ADBE"),
    "communication-services": ("GOOG", "META", "NFLX", "TMUS", "DIS", "VZ", "T", "SPOT"),
    "consumer-cyclical": ("AMZN", "TSLA", "WMT", "HD", "MCD", "BKNG", "LOW", "TJX"),
    "financial-services": ("JPM", "V", "MA", "BAC", "WFC", "GS", "MS", "AXP"),
    "healthcare": ("LLY", "UNH", "JNJ", "ABBV", "MRK", "TMO", "ABT", "ISRG"),
    "industrials": ("GE", "CAT", "RTX", "UBER", "BA", "HON", "UNP", "DE"),
    "energy": ("XOM", "CVX", "COP", "WMB", "SLB", "EOG", "OKE", "MPC"),
    "consumer-defensive": ("WMT", "COST", "PG", "KO", "PM", "PEP", "MO", "MDLZ"),
    "utilities": ("NEE", "SO", "DUK", "CEG", "AEP", "SRE", "VST", "D"),
    "real-estate": ("PLD", "AMT", "EQIX", "WELL", "SPG", "O", "DLR", "PSA"),
}
SECTOR_LABELS = {
    key: key.replace("-", " ").title() for key in SECTOR_SYMBOLS
}
SECTOR_LABELS.update({
    "all": "S&P 500",
    "basic-materials": "Materials",
})
GICS_TO_SLUG = {
    "Communication Services": "communication-services",
    "Consumer Discretionary": "consumer-cyclical",
    "Consumer Staples": "consumer-defensive",
    "Energy": "energy",
    "Financials": "financial-services",
    "Health Care": "healthcare",
    "Industrials": "industrials",
    "Information Technology": "technology",
    "Materials": "basic-materials",
    "Real Estate": "real-estate",
    "Utilities": "utilities",
}
CONSTITUENTS_URL = (
    "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/"
    "main/data/constituents.csv"
)
CACHE_TTL_SECONDS = 3600
