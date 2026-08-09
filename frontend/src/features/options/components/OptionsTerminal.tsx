import { useEffect, useMemo, useState, type FormEvent } from 'react';

import { useOptionChain } from '../hooks/useOptionChain';
import { dateLabel, mark, money } from '../lib/formatters';
import type { OptionType } from '../types';
import { GreeksChart } from './GreeksChart';
import { PositionCard } from './PositionCard';
import { OptionLifetimeChart } from './OptionLifetimeChart';
import { getEarningsCalendar } from '../../earnings/api/getEarningsCalendar';

export function OptionsTerminal() {
  const [symbol, setSymbol] = useState('AAPL');
  const [type, setType] = useState<OptionType>('call');
  const [contractIndex, setContractIndex] = useState(0);
  const [contracts, setContracts] = useState(1);
  const [costBasis, setCostBasis] = useState(0);
  const [futurePrice, setFuturePrice] = useState(100);
  const [volatility, setVolatility] = useState(30);
  const [rate, setRate] = useState(4.25);
  const [nextEarnings, setNextEarnings] = useState<string | null | undefined>(undefined);
  const { data, loading, error, load } = useOptionChain();
  const chainContracts = useMemo(
    () => data ? (type === 'call' ? data.calls : data.puts) : [],
    [data, type],
  );
  const contract = chainContracts[contractIndex];

  useEffect(() => {
    if (!data || !chainContracts.length) return;
    const nearest = chainContracts.reduce(
      (best, item, index) => Math.abs(item.strike - data.spot) < Math.abs(chainContracts[best].strike - data.spot) ? index : best,
      0,
    );
    setContractIndex(nearest);
  }, [data, type]);

  useEffect(() => {
    if (!data || !contract) return;
    setCostBasis(Number(mark(contract).toFixed(2)));
    setFuturePrice(Number(data.spot.toFixed(2)));
    setVolatility(Math.min(200, Math.max(1, contract.impliedVolatility * 100)));
  }, [data?.symbol, data?.selectedExpiration, contract?.symbol]);

  useEffect(() => {
    if (!data?.symbol) return;
    let active = true;
    setNextEarnings(undefined);
    getEarningsCalendar([data.symbol])
      .then(calendar => {
        if (!active) return;
        const upcoming = calendar.events
          .filter(event => new Date(event.earningsDate).getTime() >= Date.now())
          .sort((a, b) => a.earningsDate.localeCompare(b.earningsDate))[0];
        setNextEarnings(upcoming?.earningsDate ?? null);
      })
      .catch(() => { if (active) setNextEarnings(null); });
    return () => { active = false; };
  }, [data?.symbol]);

  const submit = (event: FormEvent) => {
    event.preventDefault();
    void load(symbol);
  };

  return <>
    <main>
      <section className="hero">
        <div>
          <p className="eyebrow">DERIVATIVES / SCENARIO ENGINE</p>
          <h1>Options risk terminal</h1>
          <p className="lede">Live chain selection, position-level P&amp;L, and Greek exposure projected through expiration.</p>
        </div>
        <form className="ticker-search" onSubmit={submit}>
          <label htmlFor="symbol">Underlying ticker</label>
          <div className="search-row">
            <input id="symbol" value={symbol} maxLength={12} onChange={event => setSymbol(event.target.value.toUpperCase())}/>
            <button disabled={loading}>{loading ? 'Loading…' : 'Load chain →'}</button>
          </div>
        </form>
      </section>
      <section className="workspace">
        {error && <div className="error" role="alert">{error}. Live chains depend on the upstream provider and can be temporarily rate-limited.</div>}
        {data && <>
          <div className="quote-strip">
            <div><span className="quote-symbol">{data.symbol}</span><span className="quote-price">{money(data.spot, data.currency)}</span><span className={`quote-change ${data.spotChange >= 0 ? 'positive' : 'negative'}`}>{data.spotChange >= 0 ? '+' : ''}{data.spotChange.toFixed(2)}%</span></div>
            <div className="quote-meta"><span className="next-earnings"><b>Next earnings</b> {nextEarnings===undefined?'Loading…':nextEarnings===null?'Unavailable':new Date(nextEarnings).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}</span><span className="dot">•</span><span>Updated {new Date(data.marketTime * 1000).toLocaleString()}</span><span className="dot">•</span><span>{data.source}</span></div>
          </div>
          <div className="controls">
            <label>Expiration<select value={data.selectedExpiration} onChange={event => void load(data.symbol, Number(event.target.value))}>{data.expirations.map(value => <option key={value} value={value}>{dateLabel(value)}</option>)}</select></label>
            <div className="segmented"><button className={type === 'call' ? 'active' : ''} onClick={() => setType('call')}>Calls</button><button className={type === 'put' ? 'active' : ''} onClick={() => setType('put')}>Puts</button></div>
            <label>Contract<select value={contractIndex} onChange={event => setContractIndex(Number(event.target.value))}>{chainContracts.map((item, index) => <option key={item.symbol} value={index}>{item.strike.toFixed(2)} strike · {money(mark(item))} · IV {(item.impliedVolatility * 100).toFixed(1)}%</option>)}</select></label>
          </div>
          {contract && <>
            <PositionCard chain={data} contract={contract} type={type} contracts={contracts} costBasis={costBasis} futurePrice={futurePrice} onContractsChange={setContracts} onCostBasisChange={setCostBasis}/>
            <GreeksChart spot={data.spot} expiration={data.selectedExpiration} contract={contract} type={type} futurePrice={futurePrice} volatility={volatility} rate={rate} contracts={contracts} costBasis={costBasis} onFuturePriceChange={setFuturePrice} onVolatilityChange={setVolatility} onRateChange={setRate}/>
            <OptionLifetimeChart contract={contract}/>
          </>}
        </>}
      </section>
    </main>
    <footer>For education and scenario analysis only. Quotes may be delayed. Not investment advice.</footer>
  </>;
}
