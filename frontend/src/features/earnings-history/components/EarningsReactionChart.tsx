import { useEffect, useMemo, useState, type MouseEvent } from 'react';

import { getEarningsReactionChart } from '../api/getEarningsHistory';
import type { EarningsReaction, EarningsReactionChartResponse } from '../types';

interface Props { symbol: string; event: EarningsReaction }
type WindowDays = 1 | 7 | 14 | 21 | 63 | 126 | 252;
const WINDOWS: { days: WindowDays; label: string }[] = [
  { days: 1, label: '1D' }, { days: 7, label: '7D' }, { days: 14, label: '14D' },
  { days: 21, label: '1M' }, { days: 63, label: '3M' },
  { days: 126, label: '6M' }, { days: 252, label: '1Y' },
];

const money = (value: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
const sessionLabel = (value: string) => new Date(value).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });

export function EarningsReactionChart({ symbol, event }: Props) {
  const [data, setData] = useState<EarningsReactionChartResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);
  const [windowDays, setWindowDays] = useState<WindowDays>(1);

  useEffect(() => {
    setData(null); setError(null); setHoverIndex(null);
    getEarningsReactionChart(symbol, event, windowDays)
      .then(setData)
      .catch(value => setError(value instanceof Error ? value.message : 'Unable to load chart'));
  }, [symbol, event.reportDate, windowDays]);

  const chart = useMemo(() => {
    if (!data?.points.length) return null;
    const W = 1000, H = 340, m = { l: 70, r: 22, t: 24, b: 58 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const values = data.points.flatMap(point => [point.low, point.high]);
    const rawMin = Math.min(...values), rawMax = Math.max(...values), pad = (rawMax - rawMin) * .12 || 1;
    const min = rawMin - pad, max = rawMax + pad;
    const x = (index: number) => m.l + index / Math.max(1, data.points.length - 1) * iw;
    const y = (value: number) => m.t + (max - value) / (max - min) * ih;
    const path = data.points.map((point, index) => `${index ? 'L' : 'M'}${x(index)},${y(point.close)}`).join(' ');
    const split = Math.max(0, data.points.findIndex(point => point.timestamp.slice(0, 10) === event.nextSessionDate.slice(0, 10)));
    const splitX = split > 0 ? (x(split - 1) + x(split)) / 2 : m.l + iw / 2;
    return { W, H, m, iw, ih, min, max, x, y, path, splitX, labelStride: Math.max(1, Math.ceil(data.points.length / 10)) };
  }, [data, event.nextSessionDate]);

  const onMove = (mouse: MouseEvent<SVGRectElement>) => {
    if (!data || !chart) return;
    const bounds = mouse.currentTarget.ownerSVGElement!.getBoundingClientRect();
    const cursor = (mouse.clientX - bounds.left) * chart.W / bounds.width;
    const index = Math.round((cursor - chart.m.l) / chart.iw * (data.points.length - 1));
    setHoverIndex(Math.max(0, Math.min(data.points.length - 1, index)));
  };
  const hovered = data && hoverIndex !== null ? data.points[hoverIndex] : null;

  return <div className="reaction-chart-panel">
    <div className="reaction-chart-head">
      <div><p className="eyebrow">SELECTED EVENT</p><h3>{symbol} · {WINDOWS.find(item => item.days === windowDays)?.label} before and after earnings</h3></div>
      <div><span>Overnight gap</span><strong className={event.changePercent >= 0 ? 'positive' : 'negative'}>{event.changePercent >= 0 ? '+' : ''}{event.changePercent.toFixed(2)}%</strong></div>
    </div>
    <div className="reaction-window-toggle" aria-label="Trading days before and after earnings">
      {WINDOWS.map(window => <button key={window.days} className={windowDays === window.days ? 'active' : ''} onClick={() => setWindowDays(window.days)}>{window.label}</button>)}
    </div>
    {error && <div className="error">{error}</div>}
    {!data && !error && <div className="earnings-state"><span className="pulse"/> Loading hourly session prices…</div>}
    {data && chart && <>
      <div className="reaction-chart-wrap">
        <svg className="reaction-chart" viewBox={`0 0 ${chart.W} ${chart.H}`} role="img" aria-label={`Hourly prices before and after ${symbol} earnings`}>
          <rect x={chart.m.l} y={chart.m.t} width={chart.splitX - chart.m.l} height={chart.ih} fill="#0f161d"/>
          <rect x={chart.splitX} y={chart.m.t} width={chart.W - chart.m.r - chart.splitX} height={chart.ih} fill="#101b18"/>
          <line className="earnings-boundary" x1={chart.splitX} x2={chart.splitX} y1={chart.m.t} y2={chart.m.t + chart.ih}/>
          {[0, 1, 2, 3, 4].map(index => { const yy = chart.m.t + chart.ih * index / 4, value = chart.max - (chart.max - chart.min) * index / 4; return <g key={index}><line className="axis" x1={chart.m.l} x2={chart.W - chart.m.r} y1={yy} y2={yy}/><text className="axis-text" x={chart.m.l - 10} y={yy + 4} textAnchor="end">{money(value)}</text></g>; })}
          <path d={chart.path} fill="none" stroke="#48e39b" strokeWidth="3"/>
          {data.points.map((point, index) => <g key={point.timestamp}><line x1={chart.x(index)} x2={chart.x(index)} y1={chart.y(point.low)} y2={chart.y(point.high)} stroke="#77838e"/><circle cx={chart.x(index)} cy={chart.y(point.close)} r="3" fill="#48e39b"/>{index % chart.labelStride === 0 && <text className="axis-text" x={chart.x(index)} y={chart.H - 15} textAnchor="middle">{new Date(point.timestamp).toLocaleDateString('en-US', { month: 'numeric', day: 'numeric' })}</text>}</g>)}
          {hovered && hoverIndex !== null && <g><line className="reaction-crosshair" x1={chart.x(hoverIndex)} x2={chart.x(hoverIndex)} y1={chart.m.t} y2={chart.m.t + chart.ih}/><circle cx={chart.x(hoverIndex)} cy={chart.y(hovered.close)} r="7" fill="#e7b45a" stroke="#080d11" strokeWidth="3"/></g>}
          <text className="session-label" x={(chart.m.l + chart.splitX) / 2} y={chart.m.t + 18} textAnchor="middle">BEFORE EARNINGS</text>
          <text className="session-label" x={(chart.splitX + chart.W - chart.m.r) / 2} y={chart.m.t + 18} textAnchor="middle">AFTER EARNINGS</text>
          <rect className="reaction-hit" x={chart.m.l} y={chart.m.t} width={chart.iw} height={chart.ih} onMouseMove={onMove} onMouseLeave={() => setHoverIndex(null)}/>
        </svg>
        {hovered && hoverIndex !== null && <div className="reaction-tooltip" style={{ left: `${Math.min(82, Math.max(18, chart.x(hoverIndex) / chart.W * 100))}%`, top: `${Math.max(4, chart.y(hovered.close) / chart.H * 100)}%` }}><span>{new Date(hovered.timestamp).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' })}</span><strong>{money(hovered.close)}</strong><small>O {money(hovered.open)} · H {money(hovered.high)}<br/>L {money(hovered.low)} · C {money(hovered.close)}</small></div>}
      </div>
      <div className="reaction-chart-foot"><span>{data.points.length} {data.interval.toLowerCase()} bars · up to {data.tradingDays} sessions each side</span><span>Move across the chart for exact prices</span><span>{data.source}</span></div>
    </>}
  </div>;
}
