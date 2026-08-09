import { useMemo, useState } from 'react';

import { useMarketResearch } from '../hooks/useMarketResearch';

const currency=(value:number|null)=>value===null?'—':new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2}).format(value);
const largeNumber=(value:number|null)=>value===null?'—':new Intl.NumberFormat('en-US',{notation:'compact',maximumFractionDigits:2}).format(value);
const ratio=(value:number|null)=>value===null?'—':value.toFixed(1);

export function MarketResearch(){
  const {sectors,selected,setSelected,page,setPage,query,setQuery,data,loading,error}=useMarketResearch();
  const [marketCapOrder,setMarketCapOrder]=useState<'asc'|'desc'>('desc');
  const pages=data?Math.max(1,Math.ceil(data.totalCount/data.pageSize)):1;
  const companies=useMemo(()=>[...(data?.companies??[])].sort((a,b)=>{
    const left=a.marketCap??(marketCapOrder==='asc'?Number.POSITIVE_INFINITY:Number.NEGATIVE_INFINITY);
    const right=b.marketCap??(marketCapOrder==='asc'?Number.POSITIVE_INFINITY:Number.NEGATIVE_INFINITY);
    return marketCapOrder==='asc'?left-right:right-left;
  }),[data?.companies,marketCapOrder]);

  return <main>
    <section className="research-hero">
      <div><p className="eyebrow">EQUITY RESEARCH / S&amp;P 500</p><h1>S&amp;P 500 market research</h1><p>Screen every index constituent by sector using capitalization, valuation, revenue, margins, and analyst expectations.</p></div>
      <label className="research-search">Find company<input value={query} placeholder="Ticker or company" onChange={event=>{setQuery(event.target.value);setPage(1)}}/></label>
    </section>
    <div className="sector-tabs" role="tablist" aria-label="Market sectors">{sectors.map(sector=><button key={sector.slug} className={selected===sector.slug?'active':''} onClick={()=>setSelected(sector.slug)}>{sector.label}<span>{sector.companyCount}</span></button>)}</div>
    <section className="research-panel">
      {loading&&<div className="earnings-state"><span className="pulse"/> Loading S&amp;P 500 fundamentals…</div>}
      {error&&<div className="error">{error}</div>}
      {data&&!loading&&<>
        <div className="research-head"><div><p className="eyebrow">{data.sector.label.toUpperCase()} / {data.totalCount} CONSTITUENTS</p><h2>Market-cap leaders</h2></div><span>{data.source}</span></div>
        <div className="research-table-wrap"><table className="research-table"><thead><tr><th>Rank</th><th>Company</th><th><button className="table-sort" onClick={()=>setMarketCapOrder(current=>current==='desc'?'asc':'desc')} aria-label={`Sort market cap ${marketCapOrder==='desc'?'ascending':'descending'}`}>Market cap <span>{marketCapOrder==='desc'?'↓':'↑'}</span></button></th><th>Price</th><th>P/E</th><th>Revenue</th><th>Net margin</th><th>Target</th><th>View</th></tr></thead><tbody>{companies.map((company,index)=><tr key={company.symbol}><td className="rank">{String((page-1)*data.pageSize+index+1).padStart(3,'0')}</td><td><strong><a href={`#/ticker/${company.symbol}`}>{company.symbol}</a></strong><span>{company.name}</span><small>{company.sector} · {company.industry}</small></td><td>{largeNumber(company.marketCap)}</td><td>{currency(company.currentPrice)}</td><td>{ratio(company.trailingPe)}</td><td>{largeNumber(company.revenue)}</td><td className={company.profitMargin!==null&&company.profitMargin>=0?'positive':'negative'}>{company.profitMargin===null?'—':`${(company.profitMargin*100).toFixed(1)}%`}</td><td>{currency(company.targetPrice)}</td><td><a href="#/options">Options →</a></td></tr>)}</tbody></table></div>
        <div className="research-pagination"><button disabled={page<=1} onClick={()=>setPage(page-1)}>← Previous</button><span>Page {page} / {pages} · {data.totalCount} companies</span><button disabled={page>=pages} onClick={()=>setPage(page+1)}>Next →</button></div>
      </>}
    </section>
  </main>;
}
