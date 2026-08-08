# OptionScope

A dependency-free options visualizer that loads a live option chain and projects
the selected contract's Black–Scholes Greeks through expiration.

## Run locally

Requires Node.js 20 or newer.

```bash
npm start
```

Open [http://localhost:4173](http://localhost:4173).

## Data and modeling

- The server proxies Cboe's public delayed option-chain endpoint and caches
  responses for 30 seconds. Quotes are delayed and the upstream endpoint can
  occasionally rate-limit.
- The chart is a scenario projection, not historical recorded Greeks. The stock
  price follows a linear path from the current quote to the user's chosen price
  at expiration. Implied volatility and the risk-free rate stay constant unless
  the user changes those controls.
- The model assumes European exercise and no dividends. It is intended for
  education and scenario analysis, not trading decisions.
