import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('./public/', import.meta.url));
const port = Number(process.env.PORT || 4173);
const cache = new Map();

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml'
};

function json(res, status, body) {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' });
  res.end(JSON.stringify(body));
}

async function cboe(symbol) {
  const response = await fetch(`https://cdn.cboe.com/api/global/delayed_quotes/options/${encodeURIComponent(symbol)}.json`, {
    headers: { 'user-agent': 'options-lifetime-visualizer/1.0', accept: 'application/json' },
    signal: AbortSignal.timeout(9000)
  });
  if (!response.ok) throw new Error(`Market data provider returned ${response.status}`);
  return response.json();
}

function parseOptionSymbol(option) {
  const match = option.match(/^(.+?)(\d{2})(\d{2})(\d{2})([CP])(\d{8})$/);
  if (!match) return null;
  const [, , yy, mm, dd, side, strike] = match;
  return {
    expiration: Date.UTC(2000 + Number(yy), Number(mm) - 1, Number(dd)) / 1000,
    type: side === 'C' ? 'call' : 'put',
    strike: Number(strike) / 1000
  };
}

async function getOptions(symbol, expiration) {
  const key = `${symbol}:${expiration || 'nearest'}`;
  const cached = cache.get(key);
  if (cached && Date.now() - cached.at < 30_000) return cached.value;
  const raw = await cboe(symbol);
  const data = raw?.data;
  if (!data?.options?.length) throw new Error('No option chain found');
  const parsed = data.options.map((item) => ({ item, details: parseOptionSymbol(item.option) })).filter((x) => x.details);
  const today = Date.now() / 1000 - 86400;
  const expirations = [...new Set(parsed.map((x) => x.details.expiration))].filter((x) => x >= today).sort((a, b) => a - b);
  const selectedExpiration = expirations.includes(Number(expiration)) ? Number(expiration) : expirations[0];
  const mapContract = ({ item, details }) => ({
    symbol: item.option,
    type: details.type,
    strike: details.strike,
    bid: item.bid,
    ask: item.ask,
    last: item.last_trade_price,
    change: item.percent_change,
    volume: item.volume || 0,
    openInterest: item.open_interest || 0,
    impliedVolatility: item.iv,
    inTheMoney: details.type === 'call' ? details.strike < data.current_price : details.strike > data.current_price,
    lastTrade: item.last_trade_time,
    publishedGreeks: { delta: item.delta, gamma: item.gamma, theta: item.theta, vega: item.vega, rho: item.rho }
  });
  const chain = parsed.filter((x) => x.details.expiration === selectedExpiration);
  const value = {
    symbol: data.symbol || symbol,
    spot: data.current_price,
    spotChange: data.price_change_percent,
    marketTime: Math.floor(new Date(raw.timestamp.replace(' ', 'T') + 'Z').getTime() / 1000),
    currency: 'USD',
    expirations,
    selectedExpiration,
    calls: chain.filter((x) => x.details.type === 'call').map(mapContract),
    puts: chain.filter((x) => x.details.type === 'put').map(mapContract),
    source: 'Cboe delayed quotes'
  };
  cache.set(key, { at: Date.now(), value });
  return value;
}

async function api(req, res, url) {
  if (url.pathname !== '/api/options') return json(res, 404, { error: 'Not found' });
  const symbol = (url.searchParams.get('symbol') || 'AAPL').trim().toUpperCase();
  if (!/^[A-Z.^-]{1,12}$/.test(symbol)) return json(res, 400, { error: 'Invalid ticker symbol' });
  const expiration = url.searchParams.get('expiration');
  try {
    json(res, 200, await getOptions(symbol, expiration));
  } catch (error) {
    json(res, 502, { error: error.message, hint: 'The upstream market-data endpoint may be rate-limited. Try again shortly.' });
  }
}

async function staticFile(res, pathname) {
  const requested = pathname === '/' ? 'index.html' : pathname.slice(1);
  const safePath = normalize(requested).replace(/^(\.\.(\/|\\|$))+/, '');
  const path = join(root, safePath);
  try {
    const info = await stat(path);
    if (!info.isFile()) throw new Error('not a file');
    const body = await readFile(path);
    res.writeHead(200, { 'content-type': mime[extname(path)] || 'application/octet-stream' });
    res.end(body);
  } catch {
    const body = await readFile(join(root, 'index.html'));
    res.writeHead(200, { 'content-type': mime['.html'] });
    res.end(body);
  }
}

createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  if (url.pathname.startsWith('/api/')) return api(req, res, url);
  return staticFile(res, url.pathname);
}).listen(port, () => console.log(`Options visualizer running at http://localhost:${port}`));
