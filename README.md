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

The repository is split into two independently runnable applications.

```text
options-dashboard/
├── frontend/
│   └── src/
│       ├── app/                  # application assembly
│       ├── components/           # shared application navigation
│       ├── features/options/     # options API, hooks, math, UI, and types
│       ├── features/earnings/    # earnings API, hook, calendar UI, and types
│       ├── features/earnings-history/ # historical reaction analysis
│       ├── features/price-history/ # price and earnings timeline
│       ├── features/research/    # sector research API, state, UI, and types
│       └── styles/               # global visual system
└── backend/
    ├── src/
    │   ├── options/              # router, schemas, client, service, and utilities
    │   ├── earnings/             # yfinance client, calendar service, and router
    │   ├── research/             # sector universes, fundamentals, and rankings
    │   ├── price_history/        # historical prices and earnings events
    │   ├── config.py             # global settings
    │   ├── exceptions.py         # shared exception handling
    │   └── main.py               # FastAPI assembly
    └── tests/options/            # tests mirror domain structure
```

The frontend follows the feature-oriented boundaries described by
[Bulletproof React](https://github.com/alan2207/bulletproof-react). The backend
uses domain packages and thin routers following
[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices).

## Setup

```bash
npm install
python3 -m venv backend/.venv
backend/.venv/bin/pip install -e 'backend[dev]'
```

Run the API and frontend in separate terminals:

```bash
npm run api
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). FastAPI documentation is
available at [http://localhost:8000/docs](http://localhost:8000/docs).

The frontend routes are `#/options`, `#/earnings`, `#/earnings-history`,
`#/price-history`, and `#/research`. The earnings API is
available at `GET /api/earnings`; an optional `symbols=AAPL,MSFT` query parameter
overrides the default watchlist.

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
