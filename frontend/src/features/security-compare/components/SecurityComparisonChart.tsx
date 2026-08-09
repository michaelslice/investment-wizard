import { useMemo, useState, type MouseEvent } from 'react';

import type { ComparisonSeries } from '../types';

const shortDate=(value:number)=>new Date(value).toLocaleDateString('en-US',{month:'short',day:'2-digit',year:'2-digit'});
const money=(value:number)=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2}).format(value);

export function SecurityComparisonChart({series,mode}:{series:ComparisonSeries[];mode:'percent'|'price'}){
  const[hoverTime,setHoverTime]=useState<number|null>(null);
  const chart=useMemo(()=>{const W=1180,H=570,m={l:70,r:76,t:34,b:58},iw=W-m.l-m.r,ih=H-m.t-m.b,available=series.filter(item=>item.prices.length);if(!available.length)return null;const first=Math.min(...available.map(item=>new Date(item.prices[0].date).getTime())),last=Math.max(...available.map(item=>new Date(item.prices.at(-1)!.date).getTime())),value=(item:ComparisonSeries,index:number)=>mode==='percent'?(item.prices[index].close/item.prices[0].close-1)*100:item.prices[index].close,values=available.flatMap(item=>item.prices.map((_,index)=>value(item,index))),rawMin=Math.min(...values),rawMax=Math.max(...values),pad=Math.max((rawMax-rawMin)*.1,mode==='percent'?2:1),min=rawMin-pad,max=rawMax+pad,x=(time:number)=>m.l+(time-first)/Math.max(1,last-first)*iw,y=(number:number)=>m.t+(max-number)/(max-min)*ih,paths=available.map(item=>({item,path:item.prices.map((point,index)=>`${index?'L':'M'}${x(new Date(point.date).getTime())},${y(value(item,index))}`).join(' ')}));return{W,H,m,iw,ih,first,last,min,max,x,y,value,paths}},[series,mode]);
  if(!chart)return <div className="compare-empty">Add a ticker to begin comparing performance.</div>;
  const onMove=(event:MouseEvent<SVGRectElement>)=>{const bounds=event.currentTarget.ownerSVGElement!.getBoundingClientRect(),cursor=(event.clientX-bounds.left)*chart.W/bounds.width;setHoverTime(chart.first+(cursor-chart.m.l)/chart.iw*(chart.last-chart.first))};
  const hovered=hoverTime===null?[]:series.filter(item=>item.prices.length).map(item=>{let index=0;item.prices.forEach((point,candidate)=>{if(Math.abs(new Date(point.date).getTime()-hoverTime)<Math.abs(new Date(item.prices[index].date).getTime()-hoverTime))index=candidate});return{item,index,point:item.prices[index],value:chart.value(item,index)}});
  const focusTime=hovered.length?new Date(hovered[0].point.date).getTime():null;
  return <div className="compare-chart-wrap"><svg className="compare-chart" viewBox={`0 0 ${chart.W} ${chart.H}`} role="img" aria-label="Historical multiple security comparison">
    {[0,1,2,3,4,5].map(index=>{const yy=chart.m.t+chart.ih*index/5,value=chart.max-(chart.max-chart.min)*index/5;return <g key={index}><line className="compare-grid" x1={chart.m.l} x2={chart.W-chart.m.r} y1={yy} y2={yy}/><text className="compare-axis-text" x={chart.W-chart.m.r+12} y={yy+4}>{mode==='percent'?`${value>=0?'+':''}${value.toFixed(1)}%`:money(value)}</text></g>})}
    {[0,1,2,3,4].map(index=>{const time=chart.first+(chart.last-chart.first)*index/4;return <text key={index} className="compare-axis-text" x={chart.x(time)} y={chart.H-20} textAnchor={index===0?'start':index===4?'end':'middle'}>{shortDate(time)}</text>})}
    {mode==='percent'&&chart.min<0&&chart.max>0?<line className="compare-zero" x1={chart.m.l} x2={chart.W-chart.m.r} y1={chart.y(0)} y2={chart.y(0)}/>:null}
    {chart.paths.map(({item,path})=><path key={item.symbol} d={path} className="compare-series" style={{stroke:item.color}}/>)}
    {focusTime!==null?<line className="compare-crosshair" x1={chart.x(focusTime)} x2={chart.x(focusTime)} y1={chart.m.t} y2={chart.m.t+chart.ih}/>:null}
    {hovered.map(({item,point,value})=><circle key={item.symbol} cx={chart.x(new Date(point.date).getTime())} cy={chart.y(value)} r="5" className="compare-focus" style={{fill:item.color}}/>)}
    <rect className="compare-hit" x={chart.m.l} y={chart.m.t} width={chart.iw} height={chart.ih} onMouseMove={onMove} onMouseLeave={()=>setHoverTime(null)}/>
  </svg>{hovered.length?<div className="compare-tooltip" style={{left:`${Math.min(80,Math.max(20,chart.x(focusTime!)/chart.W*100))}%`}}><time>{shortDate(focusTime!)}</time>{hovered.map(({item,point,value})=><div key={item.symbol}><i style={{background:item.color}}/><strong>{item.symbol}</strong><span>{mode==='percent'?`${value>=0?'+':''}${value.toFixed(2)}%`:money(value)}</span><small>{money(point.close)}</small></div>)}</div>:null}</div>
}
