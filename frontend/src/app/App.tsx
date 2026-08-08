import { useEffect, useState } from 'react';
import { AppNavbar } from '../components/AppNavbar';
import { EarningsCalendar } from '../features/earnings/components/EarningsCalendar';
import { OptionsTerminal } from '../features/options/components/OptionsTerminal';
import { MarketResearch } from '../features/research/components/MarketResearch';

const getPage = (): 'earnings' | 'options' | 'research' => window.location.hash === '#/earnings' ? 'earnings' : window.location.hash === '#/research' ? 'research' : 'options';

export function App() {
  const [page, setPage] = useState(getPage);
  useEffect(() => { const update = () => setPage(getPage()); window.addEventListener('hashchange', update); return () => window.removeEventListener('hashchange', update); }, []);
  return <><AppNavbar activePage={page}/>{page === 'earnings' ? <EarningsCalendar/> : page === 'research' ? <MarketResearch/> : <OptionsTerminal/>}</>;
}
