interface Props { activePage: 'chat' | 'compare' | 'options' | 'earnings' | 'earnings-history' | 'price-history' | 'research' | 'ticker' | 'watchlist' }

const links = [
  ['options', 'Options terminal'],
  ['earnings', 'Upcoming earnings'],
  ['earnings-history', 'Earnings reactions'],
  ['price-history', 'Price history'],
  ['compare', 'Compare'],
  ['research', 'Market research'],
  ['watchlist', 'Watchlist'],
  ['chat', 'AI research'],
] as const;

export function AppNavbar({ activePage }: Props) {
  return <header className="topbar">
    <a className="brand" href="#/options"><span className="brand-mark">O/</span><span>OPTIONSCOPE</span><small>RISK TERMINAL</small></a>
    <nav className="primary-nav" aria-label="Primary navigation">
      {links.map(([page, label]) => <a key={page} className={activePage === page || activePage === 'ticker' && page === 'research' ? 'active' : ''} href={`#/${page}`}>{label}</a>)}
    </nav>
    <div className="market-state"><span className="pulse"/><span>Market data</span></div>
  </header>;
}
