import { useEffect, useState } from 'react';
import { AppNavbar } from '../components/AppNavbar';
import { EarningsCalendar } from '../features/earnings/components/EarningsCalendar';
import { EarningsHistory } from '../features/earnings-history/components/EarningsHistory';
import { OptionsTerminal } from '../features/options/components/OptionsTerminal';
import { MarketResearch } from '../features/research/components/MarketResearch';
import { PriceHistory } from '../features/price-history/components/PriceHistory';
import { StockWatchlist } from '../features/watchlist/components/StockWatchlist';
import { TickerResearch } from '../features/ticker-research/components/TickerResearch';
import { ResearchChat } from '../features/chat/components/ResearchChat';
import { SecurityCompare } from '../features/security-compare/components/SecurityCompare';

const getPage = (): 'chat' | 'compare' | 'earnings' | 'earnings-history' | 'options' | 'price-history' | 'research' | 'ticker' | 'watchlist' => window.location.hash === '#/chat' ? 'chat' : window.location.hash === '#/compare' ? 'compare' : window.location.hash === '#/earnings' ? 'earnings' : window.location.hash === '#/earnings-history' ? 'earnings-history' : window.location.hash === '#/price-history' ? 'price-history' : window.location.hash === '#/research' ? 'research' : window.location.hash.startsWith('#/ticker/') ? 'ticker' : window.location.hash === '#/watchlist' ? 'watchlist' : 'options';
const getTicker=()=>decodeURIComponent(window.location.hash.split('/')[2]??'AAPL').toUpperCase();

export function App() {
  const [page, setPage] = useState(getPage);
  useEffect(() => { const update = () => setPage(getPage()); window.addEventListener('hashchange', update); return () => window.removeEventListener('hashchange', update); }, []);
  return <><AppNavbar activePage={page}/>{page === 'chat' ? <ResearchChat/> : page === 'compare' ? <SecurityCompare/> : page === 'earnings' ? <EarningsCalendar/> : page === 'earnings-history' ? <EarningsHistory/> : page === 'price-history' ? <PriceHistory/> : page === 'research' ? <MarketResearch/> : page === 'ticker' ? <TickerResearch symbol={getTicker()}/> : page === 'watchlist' ? <StockWatchlist/> : <OptionsTerminal/>}</>;
}
