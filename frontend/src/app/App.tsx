import { useEffect, useState } from 'react';
import { AppNavbar } from '../components/AppNavbar';
import { EarningsCalendar } from '../features/earnings/components/EarningsCalendar';
import { EarningsHistory } from '../features/earnings-history/components/EarningsHistory';
import { OptionsTerminal } from '../features/options/components/OptionsTerminal';
import { MarketResearch } from '../features/research/components/MarketResearch';
import { PriceHistory } from '../features/price-history/components/PriceHistory';

const getPage = (): 'earnings' | 'earnings-history' | 'options' | 'price-history' | 'research' => window.location.hash === '#/earnings' ? 'earnings' : window.location.hash === '#/earnings-history' ? 'earnings-history' : window.location.hash === '#/price-history' ? 'price-history' : window.location.hash === '#/research' ? 'research' : 'options';

export function App() {
  const [page, setPage] = useState(getPage);
  useEffect(() => { const update = () => setPage(getPage()); window.addEventListener('hashchange', update); return () => window.removeEventListener('hashchange', update); }, []);
  return <><AppNavbar activePage={page}/>{page === 'earnings' ? <EarningsCalendar/> : page === 'earnings-history' ? <EarningsHistory/> : page === 'price-history' ? <PriceHistory/> : page === 'research' ? <MarketResearch/> : <OptionsTerminal/>}</>;
}
