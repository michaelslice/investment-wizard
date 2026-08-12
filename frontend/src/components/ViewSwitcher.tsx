import { useEffect, useMemo, useRef, useState } from 'react';
import { useEnabledViews, type ViewId } from '../app/viewPreferences';

const VIEWS=[
  {label:'Options terminal',description:'Option chains, Greeks, scenarios, and contract history',href:'#/options',match:(hash:string)=>!hash||hash==='#/options'},
  {label:'Options chain',description:'Calls and puts aligned across strikes and expirations',href:'#/chain',match:(hash:string)=>hash==='#/chain'},
  {label:'The Eye',description:'Multi-symbol options contract scanner and liquidity screener',href:'#/eye',match:(hash:string)=>hash==='#/eye'},
  {label:'Options strategy lab',description:'Multi-leg payoff and contract pricing simulator',href:'#/simulator',match:(hash:string)=>hash==='#/simulator'},
  {label:'Upcoming earnings',description:'Forward earnings calendar and event schedule',href:'#/earnings',match:(hash:string)=>hash==='#/earnings'},
  {label:'Earnings reactions',description:'Historical before-and-after earnings performance',href:'#/earnings-history',match:(hash:string)=>hash==='#/earnings-history'},
  {label:'Price history',description:'Historical prices with earnings events',href:'#/price-history',match:(hash:string)=>hash==='#/price-history'},
  {label:'1-day performance evaluator',description:'Daily gaps, session returns, excursions, ranges, and weekday tendencies',href:'#/daily-performance',match:(hash:string)=>hash==='#/daily-performance'},
  {label:'Security compare',description:'Normalized multi-security performance chart',href:'#/compare',match:(hash:string)=>hash==='#/compare'},
  {label:'Market research',description:'S&P 500 sector and company research',href:'#/research',match:(hash:string)=>hash==='#/research'||hash.startsWith('#/ticker/')},
  {label:'Watchlist',description:'Browser-local equities watchlist',href:'#/watchlist',match:(hash:string)=>hash==='#/watchlist'},
  {label:'Ticker focus',description:'Minimal current-price board for selected securities',href:'#/focus',match:(hash:string)=>hash==='#/focus'},
  {label:'Institutional holders',description:'Ownership treemap and institutional position table',href:'#/holders',match:(hash:string)=>hash==='#/holders'},
  {label:'Net worth tracker',description:'Local brokerage, retirement, banking, and savings balances',href:'#/net-worth',match:(hash:string)=>hash==='#/net-worth'},
  {label:'Kelly Criterion lab',description:'Position sizing and Monte Carlo capital-path simulator',href:'#/kelly',match:(hash:string)=>hash==='#/kelly'},
  {label:'Real estate investing',description:'Screen active properties and model acquisition financing',href:'#/real-estate',match:(hash:string)=>hash==='#/real-estate'},
  {label:'Investment sandbox',description:'Arrange multiple tools in a draggable persistent workspace',href:'#/sandbox',match:(hash:string)=>hash==='#/sandbox'},
  {label:'Trade journal',description:'Investment theses, risk plans, and reviews',href:'#/journal',match:(hash:string)=>hash==='#/journal'},
  {label:'AI research',description:'OpenAI assistant with investment-wizard MCP tools',href:'#/chat',match:(hash:string)=>hash==='#/chat'},
];

export function ViewSwitcher(){
  const enabled=useEnabledViews(),[open,setOpen]=useState(false),[selected,setSelected]=useState(0),[query,setQuery]=useState(''),inputRef=useRef<HTMLInputElement>(null),available=useMemo(()=>VIEWS.filter(view=>enabled.includes(view.href.slice(2) as ViewId)),[enabled]),filtered=useMemo(()=>{const term=query.trim().toLowerCase();return term?available.filter(view=>`${view.label} ${view.description}`.toLowerCase().includes(term)):available},[query,available]);
  useEffect(()=>{if(open)inputRef.current?.focus()},[open]);
  useEffect(()=>{const down=(event:KeyboardEvent)=>{if(!open&&(event.key==='~'||event.key==='`')&&!event.ctrlKey&&!event.metaKey&&!event.altKey){event.preventDefault();setQuery('');setSelected(Math.max(0,available.findIndex(view=>view.match(window.location.hash))));setOpen(true);return}if(!open)return;if(event.key==='ArrowDown'){event.preventDefault();setSelected(index=>(index+1)%Math.max(1,filtered.length))}else if(event.key==='ArrowUp'){event.preventDefault();setSelected(index=>(index-1+Math.max(1,filtered.length))%Math.max(1,filtered.length))}else if(event.key==='Enter'&&filtered[selected]){event.preventDefault();window.location.hash=filtered[selected].href;setOpen(false)}else if(event.key==='Escape'){event.preventDefault();setOpen(false)}};window.addEventListener('keydown',down);return()=>window.removeEventListener('keydown',down)},[open,selected,filtered,available]);
  if(!open)return null;
  return <div className="view-switcher-backdrop" role="presentation" onMouseDown={event=>{if(event.target===event.currentTarget)setOpen(false)}}><section className="view-switcher" role="dialog" aria-modal="true" aria-label="Switch application view"><header><div><span className="brand-mark">I/W</span><div><strong>GO TO VIEW</strong><small>Type a view name</small></div></div><kbd>~</kbd></header><div className="view-switcher-search"><span>›</span><input ref={inputRef} value={query} onChange={event=>{setQuery(event.target.value);setSelected(0)}} aria-label="Search application views" placeholder="Search views…" autoComplete="off"/><kbd>ESC</kbd></div><div className="view-switcher-list" role="listbox" aria-label="Available views">{filtered.length?filtered.map((view,index)=><button key={view.href} role="option" aria-selected={selected===index} className={selected===index?'active':''} onMouseEnter={()=>setSelected(index)} onClick={()=>{window.location.hash=view.href;setOpen(false)}}><b>{String(VIEWS.indexOf(view)+1).padStart(2,'0')}</b><span><strong>{view.label}</strong><small>{view.description}</small></span><i>{selected===index?'↵':'›'}</i></button>):<div className="view-switcher-empty">No matching views</div>}</div><footer><span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span><span><kbd>Enter</kbd> Open</span><span><kbd>Esc</kbd> Close</span><span>Type to filter</span></footer></section></div>
}
