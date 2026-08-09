# OptionScope

OptionScope is a live options risk terminal with position-level P&L simulation
and Black–Scholes Greek projections through expiration. Its shared navbar also
provides an upcoming earnings calendar for the configured stock watchlist.
It also includes sector-based market research ranked by live market capitalization.
Historical earnings event studies compare each pre-report close with the first
regular-session open after results.
The price-history timeline overlays reported and upcoming earnings on adjusted
daily stock prices.

## Architecture

The repository contains independently runnable frontend, API, and MCP applications.

```text
options-dashboard/
├── frontend/
│   └── src/
│       ├── app/                  # application assembly
│       ├── components/           # shared application navigation
│       ├── features/options/     # options API, hooks, math, UI, and types
│       ├── features/chat/        # OpenAI + MCP research conversation UI
│       ├── features/earnings/    # earnings API, hook, calendar UI, and types
│       ├── features/earnings-history/ # historical reaction analysis
│       ├── features/price-history/ # price and earnings timeline
│       ├── features/research/    # sector research API, state, UI, and types
│       └── styles/               # global visual system
├── backend/
    ├── src/
    │   ├── options/              # router, schemas, client, service, and utilities
    │   ├── chat/                 # OpenAI agent, MCP bridge, schemas, and router
    │   ├── earnings/             # yfinance client, calendar service, and router
    │   ├── research/             # sector universes, fundamentals, and rankings
    │   ├── price_history/        # historical prices and earnings events
    │   ├── config.py             # global settings
    │   ├── exceptions.py         # shared exception handling
    │   └── main.py               # FastAPI assembly
    └── tests/options/            # tests mirror domain structure
└── mcp/                          # FastMCP tools and async client example
```

The frontend follows the feature-oriented boundaries described by
[Bulletproof React](https://github.com/alan2207/bulletproof-react). The backend
uses domain packages and thin routers following
[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices).
The `mcp/` package exposes the same read-only research capabilities to LLM
agents over the Model Context Protocol.

## Setup

```bash
npm install
python3 -m venv backend/.venv
backend/.venv/bin/pip install -e 'backend[dev]'
cp backend/.env.example backend/.env
```

Edit `backend/.env` and replace the placeholder with your OpenAI API key. The
key is read only by FastAPI and is never sent to or stored by the browser.

Run the API and frontend in separate terminals:

```bash
npm run api
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). FastAPI documentation is
available at [http://localhost:8000/docs](http://localhost:8000/docs).

The frontend routes are `#/options`, `#/earnings`, `#/earnings-history`, `#/compare`,
`#/price-history`, `#/research`, `#/ticker/{symbol}`, and `#/watchlist`. The earnings API is
available at `GET /api/earnings`; an optional `symbols=AAPL,MSFT` query parameter
overrides the default watchlist.

The research assistant is available at `#/chat`. It sends conversation history
to `POST /api/chat`; the API invokes OpenAI and gives the agent access to the
read-only OptionScope MCP server over a local stdio connection.

Historical reactions are available from
`GET /api/earnings/history/{symbol}?limit=12`. The response includes report
timing, the last close before reporting, the first post-report open, dollar and
percentage changes, 100-share P&L, and EPS surprise.

Selecting a historical event calls
`GET /api/earnings/history/{symbol}/chart?before_session=YYYY-MM-DD&next_session=YYYY-MM-DD`
for hourly OHLCV bars spanning the complete regular sessions before and after
the earnings report.

Market research exposes `GET /api/research/sectors` for the sector catalog and
`GET /api/research/sectors/{sector}` for companies ranked by market cap.
Watchlist fundamentals use `GET /api/research/companies?symbols=AAPL,MSFT`;
saved symbols remain client-side in browser local storage.
Ticker dossiers use `GET /api/research/tickers/{symbol}` for valuation, growth,
profitability, balance-sheet, cash-flow, ownership, and analyst metrics.

The combined stock timeline is available from
`GET /api/prices/{symbol}?period=1y`. Supported periods are `6mo`, `1y`, `3y`,
`5y`, `10y`, and `max`; the response contains daily OHLCV bars plus all
available reported and upcoming earnings events.

## Verification

```bash
npm run build
backend/.venv/bin/python -m pytest backend/tests
backend/.venv/bin/ruff check backend/src backend/tests
```

## Data and modeling

- The async FastAPI service retrieves Cboe delayed option quotes and caches raw
  chains for 30 seconds.
- Earnings dates reuse the original `yfinance.Ticker(...).calendar` workflow,
  run blocking provider calls in worker threads with bounded concurrency, and
  cache calendars for 15 minutes.
- Sector research reuses the original yfinance company-info and financial-metric
  workflow. Calls run with bounded concurrency and sector results cache for one hour.
- The scenario engine interpolates from the current underlying price to the
  selected expiration price and computes option value plus Delta, Gamma, Theta,
  Vega, and Rho with Black–Scholes.
- The model assumes European exercise, constant volatility/rate, and no
  dividends. It is intended for education and scenario analysis.
