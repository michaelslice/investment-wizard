from pydantic import BaseModel, ConfigDict, Field


class SectorSummary(BaseModel):
    slug: str
    label: str
    company_count: int = Field(alias="companyCount")


class CompanyResearch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    name: str
    sector: str
    industry: str
    market_cap: int | None = Field(alias="marketCap")
    current_price: float | None = Field(alias="currentPrice")
    trailing_pe: float | None = Field(alias="trailingPe")
    revenue: int | None
    profit_margin: float | None = Field(alias="profitMargin")
    target_price: float | None = Field(alias="targetPrice")
    recommendation: str | None


class SectorResearch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sector: SectorSummary
    companies: list[CompanyResearch]
    total_count: int = Field(alias="totalCount")
    page: int
    page_size: int = Field(alias="pageSize")
    source: str = "S&P 500 roster + Yahoo Finance via yfinance"


class TickerResearch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbol: str
    name: str
    description: str | None = None
    sector: str | None = None
    industry: str | None = None
    website: str | None = None
    country: str | None = None
    employees: int | None = None
    currency: str = "USD"
    current_price: float | None = Field(None, alias="currentPrice")
    previous_close: float | None = Field(None, alias="previousClose")
    market_cap: int | None = Field(None, alias="marketCap")
    enterprise_value: int | None = Field(None, alias="enterpriseValue")
    fifty_two_week_high: float | None = Field(None, alias="fiftyTwoWeekHigh")
    fifty_two_week_low: float | None = Field(None, alias="fiftyTwoWeekLow")
    beta: float | None = None
    trailing_pe: float | None = Field(None, alias="trailingPe")
    forward_pe: float | None = Field(None, alias="forwardPe")
    peg_ratio: float | None = Field(None, alias="pegRatio")
    price_to_sales: float | None = Field(None, alias="priceToSales")
    price_to_book: float | None = Field(None, alias="priceToBook")
    enterprise_to_revenue: float | None = Field(None, alias="enterpriseToRevenue")
    enterprise_to_ebitda: float | None = Field(None, alias="enterpriseToEbitda")
    revenue: int | None = None
    revenue_growth: float | None = Field(None, alias="revenueGrowth")
    gross_profit: int | None = Field(None, alias="grossProfit")
    ebitda: int | None = None
    net_income: int | None = Field(None, alias="netIncome")
    earnings_growth: float | None = Field(None, alias="earningsGrowth")
    diluted_eps: float | None = Field(None, alias="dilutedEps")
    gross_margin: float | None = Field(None, alias="grossMargin")
    operating_margin: float | None = Field(None, alias="operatingMargin")
    profit_margin: float | None = Field(None, alias="profitMargin")
    return_on_assets: float | None = Field(None, alias="returnOnAssets")
    return_on_equity: float | None = Field(None, alias="returnOnEquity")
    total_cash: int | None = Field(None, alias="totalCash")
    total_debt: int | None = Field(None, alias="totalDebt")
    debt_to_equity: float | None = Field(None, alias="debtToEquity")
    current_ratio: float | None = Field(None, alias="currentRatio")
    quick_ratio: float | None = Field(None, alias="quickRatio")
    operating_cash_flow: int | None = Field(None, alias="operatingCashFlow")
    free_cash_flow: int | None = Field(None, alias="freeCashFlow")
    dividend_yield: float | None = Field(None, alias="dividendYield")
    payout_ratio: float | None = Field(None, alias="payoutRatio")
    shares_outstanding: int | None = Field(None, alias="sharesOutstanding")
    float_shares: int | None = Field(None, alias="floatShares")
    shares_short: int | None = Field(None, alias="sharesShort")
    short_ratio: float | None = Field(None, alias="shortRatio")
    held_by_insiders: float | None = Field(None, alias="heldByInsiders")
    held_by_institutions: float | None = Field(None, alias="heldByInstitutions")
    target_low: float | None = Field(None, alias="targetLow")
    target_mean: float | None = Field(None, alias="targetMean")
    target_high: float | None = Field(None, alias="targetHigh")
    recommendation: str | None = None
    analyst_opinions: int | None = Field(None, alias="analystOpinions")
    source: str = "Yahoo Finance via yfinance"
