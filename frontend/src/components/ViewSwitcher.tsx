import { useEffect, useMemo, useRef, useState } from 'react';

const VIEWS=[
  {label:'Options terminal',description:'Option chains, Greeks, scenarios, and contract history',href:'#/options',match:(hash:string)=>!hash||hash==='#/options'},
  {label:'Options chain',description:'Calls and puts aligned across strikes and expirations',href:'#/chain',match:(hash:string)=>hash==='#/chain'},
  {label:'Options strategy lab',description:'Multi-leg payoff and contract pricing simulator',href:'#/simulator',match:(hash:string)=>hash==='#/simulator'},
  {label:'Upcoming earnings',description:'Forward earnings calendar and event schedule',href:'#/earnings',match:(hash:string)=>hash==='#/earnings'},
  {label:'Earnings reactions',description:'Historical before-and-after earnings performance',href:'#/earnings-history',match:(hash:string)=>hash==='#/earnings-history'},
  {label:'Price history',description:'Historical prices with earnings events',href:'#/price-history',match:(hash:string)=>hash==='#/price-history'},
  {label:'Security compare',description:'Normalized multi-security performance chart',href:'#/compare',match:(hash:string)=>hash==='#/compare'},
  {label:'Market research',description:'S&P 500 sector and company research',href:'#/research',match:(hash:string)=>hash==='#/research'||hash.startsWith('#/ticker/')},
  {label:'Watchlist',description:'Browser-local equities watchlist',href:'#/watchlist',match:(hash:string)=>hash==='#/watchlist'},
  {label:'Ticker focus',description:'Minimal current-price board for selected securities',href:'#/focus',match:(hash:string)=>hash==='#/focus'},
  {label:'Institutional holders',description:'Ownership treemap and institutional position table',href:'#/holders',match:(hash:string)=>hash==='#/holders'},
  {label:'Trade journal',description:'Investment theses, risk plans, and reviews',href:'#/journal',match:(hash:string)=>hash==='#/journal'},
  {label:'AI research',description:'OpenAI assistant with OptionScope MCP tools',href:'#/chat',match:(hash:string)=>hash==='#/chat'},
];

export function ViewSwitcher(){
  const[open,setOpen]=useState(false),[selected,setSelected]=useState(0),[query,setQuery]=useState(''),inputRef=useRef<HTMLInputElement>(null),filtered=useMemo(()=>{const term=query.trim().toLowerCase();return term?VIEWS.filter(view=>`${view.label} ${view.description}`.toLowerCase().includes(term)):VIEWS},[query]);
  useEffect(()=>{if(open)inputRef.current?.focus()},[open]);
  useEffect(()=>{const down=(event:KeyboardEvent)=>{if(!open&&(event.key==='~'||event.key==='`')&&!event.ctrlKey&&!event.metaKey&&!event.altKey){event.preventDefault();setQuery('');setSelected(Math.max(0,VIEWS.findIndex(view=>view.match(window.location.hash))));setOpen(true);return}if(!open)return;if(event.key==='ArrowDown'){event.preventDefault();setSelected(index=>(index+1)%Math.max(1,filtered.length))}else if(event.key==='ArrowUp'){event.preventDefault();setSelected(index=>(index-1+Math.max(1,filtered.length))%Math.max(1,filtered.length))}else if(event.key==='Enter'&&filtered[selected]){event.preventDefault();window.location.hash=filtered[selected].href;setOpen(false)}else if(event.key==='Escape'){event.preventDefault();setOpen(false)}};window.addEventListener('keydown',down);return()=>window.removeEventListener('keydown',down)},[open,selected,filtered]);
  if(!open)return null;
  return <div className="view-switcher-backdrop" role="presentation" onMouseDown={event=>{if(event.target===event.currentTarget)setOpen(false)}}><section className="view-switcher" role="dialog" aria-modal="true" aria-label="Switch application view"><header><div><span className="brand-mark">O/</span><div><strong>GO TO VIEW</strong><small>Type a view name</small></div></div><kbd>~</kbd></header><div className="view-switcher-search"><span>›</span><input ref={inputRef} value={query} onChange={event=>{setQuery(event.target.value);setSelected(0)}} aria-label="Search application views" placeholder="Search views…" autoComplete="off"/><kbd>ESC</kbd></div><div className="view-switcher-list" role="listbox" aria-label="Available views">{filtered.length?filtered.map((view,index)=><button key={view.href} role="option" aria-selected={selected===index} className={selected===index?'active':''} onMouseEnter={()=>setSelected(index)} onClick={()=>{window.location.hash=view.href;setOpen(false)}}><b>{String(VIEWS.indexOf(view)+1).padStart(2,'0')}</b><span><strong>{view.label}</strong><small>{view.description}</small></span><i>{selected===index?'↵':'›'}</i></button>):<div className="view-switcher-empty">No matching views</div>}</div><footer><span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span><span><kbd>Enter</kbd> Open</span><span><kbd>Esc</kbd> Close</span><span>Type to filter</span></footer></section></div>
}
