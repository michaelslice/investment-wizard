interface Props { activePage: 'chain' | 'chat' | 'compare' | 'daily-performance' | 'eye' | 'focus' | 'holders' | 'journal' | 'kelly' | 'net-worth' | 'options' | 'real-estate' | 'sandbox' | 'simulator' | 'earnings' | 'earnings-history' | 'price-history' | 'research' | 'ticker' | 'watchlist' }

const links = [
  ['options', 'Options terminal'],
  ['chain', 'Options chain'],
  ['eye', 'The Eye'],
  ['simulator', 'Strategy lab'],
  ['earnings', 'Upcoming earnings'],
  ['earnings-history', 'Earnings reactions'],
  ['price-history', 'Price history'],
  ['daily-performance', '1-day evaluator'],
  ['compare', 'Compare'],
  ['research', 'Market research'],
  ['watchlist', 'Watchlist'],
  ['focus', 'Focus'],
  ['holders', 'Holders'],
  ['net-worth', 'Net worth'],
  ['kelly', 'Kelly lab'],
  ['real-estate', 'Real estate'],
  ['sandbox', 'Sandbox'],
  ['journal', 'Trade journal'],
  ['chat', 'AI research'],
] as const;

export function AppNavbar({ activePage }: Props) {
  const enabled=useEnabledViews(),[settingsOpen,setSettingsOpen]=useState(false);
  return <header className="topbar">
    <a className="brand" href="#/options"><span className="brand-mark">I/W</span><span>investment-wizard</span><small>RISK TERMINAL</small></a>
    <nav className="primary-nav" aria-label="Primary navigation">
      {links.filter(([page])=>enabled.includes(page)).map(([page, label]) => <a key={page} className={activePage === page || activePage === 'ticker' && page === 'research' ? 'active' : ''} href={`#/${page}`}>{label}</a>)}
    </nav>
    <div className="market-state"><span className="pulse"/><span>Market data</span><button className="settings-trigger" onClick={()=>setSettingsOpen(true)} aria-label="Application settings" title="Application settings">⚙</button></div>
    <AppSettings open={settingsOpen} onClose={()=>setSettingsOpen(false)}/>
  </header>;
}
import { useState } from 'react';
import { useEnabledViews } from '../app/viewPreferences';
import { AppSettings } from './AppSettings';
