interface Props { activePage: 'options' | 'earnings' | 'earnings-history' | 'price-history' | 'research' }

const links = [
  ['options', 'Options terminal'],
  ['earnings', 'Upcoming earnings'],
  ['earnings-history', 'Earnings reactions'],
  ['price-history', 'Price history'],
  ['research', 'Market research'],
] as const;

export function AppNavbar({ activePage }: Props) {
  return <header className="topbar">
    <a className="brand" href="#/options"><span className="brand-mark">O/</span><span>OPTIONSCOPE</span><small>RISK TERMINAL</small></a>
    <nav className="primary-nav" aria-label="Primary navigation">
      {links.map(([page, label]) => <a key={page} className={activePage === page ? 'active' : ''} href={`#/${page}`}>{label}</a>)}
    </nav>
    <div className="market-state"><span className="pulse"/><span>Market data</span></div>
  </header>;
}
