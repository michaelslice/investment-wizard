const $ = (id) => document.getElementById(id);
const state = { data: null, type: 'call', contract: null, greek: 'delta' };
const greekMeta = {
  delta: { label: 'Delta', digits: 3 }, gamma: { label: 'Gamma', digits: 4 },
  theta: { label: 'Theta', digits: 3 }, vega: { label: 'Vega', digits: 3 },
  rho: { label: 'Rho', digits: 3 }
};

function normalPdf(x) { return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI); }
function normalCdf(x) {
  const k = 1 / (1 + 0.2316419 * Math.abs(x));
  const p = normalPdf(x) * (0.319381530*k - 0.356563782*k**2 + 1.781477937*k**3 - 1.821255978*k**4 + 1.330274429*k**5);
  return x >= 0 ? 1 - p : p;
}
function greeks(S, K, T, r, sigma, type) {
  T = Math.max(T, 1 / 36500); sigma = Math.max(sigma, .0001);
  const sqrtT = Math.sqrt(T), d1 = (Math.log(S/K) + (r + sigma*sigma/2)*T)/(sigma*sqrtT), d2 = d1-sigma*sqrtT;
  const pdf = normalPdf(d1), disc = Math.exp(-r*T), call = type === 'call';
  const delta = call ? normalCdf(d1) : normalCdf(d1)-1;
  const gamma = pdf/(S*sigma*sqrtT);
  const thetaAnnual = -(S*pdf*sigma)/(2*sqrtT) + (call ? -r*K*disc*normalCdf(d2) : r*K*disc*normalCdf(-d2));
  const vega = S*pdf*sqrtT/100;
  const rho = (call ? K*T*disc*normalCdf(d2) : -K*T*disc*normalCdf(-d2))/100;
  return { delta, gamma, theta: thetaAnnual/365, vega, rho };
}
function money(x) { return Number.isFinite(x) ? new Intl.NumberFormat('en-US',{style:'currency',currency:state.data?.currency||'USD'}).format(x) : '—'; }
function compact(x) { return Number.isFinite(x) ? new Intl.NumberFormat('en-US',{notation:'compact'}).format(x) : '—'; }
function dateLabel(epoch) { return new Date(epoch*1000).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}); }

async function loadChain(symbol, expiration) {
  setLoading(true); $('error').classList.add('hidden');
  try {
    const query = new URLSearchParams({ symbol }); if (expiration) query.set('expiration', expiration);
    const response = await fetch(`/api/options?${query}`); const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Unable to load option chain');
    state.data = data; renderQuote(); renderExpirations(); renderContracts();
    $('data-state').textContent = 'Market data connected'; document.querySelector('.pulse').classList.remove('stale');
  } catch (error) {
    $('error').textContent = `${error.message}. Live chains depend on the upstream provider and can be temporarily rate-limited.`;
    $('error').classList.remove('hidden'); $('data-state').textContent = 'Market data unavailable'; document.querySelector('.pulse').classList.add('stale');
  } finally { setLoading(false); }
}
function setLoading(on) { $('symbol-form').querySelector('button').disabled = on; $('symbol-form').querySelector('button').textContent = on ? 'Loading…' : 'Load chain →'; }
function renderQuote() {
  const d=state.data; $('quote-symbol').textContent=d.symbol; $('quote-price').textContent=money(d.spot);
  const ch=Number(d.spotChange); $('quote-change').textContent=Number.isFinite(ch)?`${ch>=0?'+':''}${ch.toFixed(2)}%`:'—'; $('quote-change').className=`quote-change ${ch>=0?'positive':'negative'}`;
  $('quote-time').textContent=d.marketTime?`Updated ${new Date(d.marketTime*1000).toLocaleString()}`:'Quote time unavailable'; $('quote-source').textContent=d.source;
  const floor=Math.max(.01,Math.floor(d.spot*.5)),ceiling=Math.ceil(d.spot*1.5); $('future-price').value=d.spot.toFixed(2); $('future-price-slider').min=floor; $('future-price-slider').max=ceiling; $('future-price-slider').value=d.spot;
}
function renderExpirations() {
  const select=$('expiration'), selected=state.data.selectedExpiration; select.innerHTML=state.data.expirations.map(x=>`<option value="${x}" ${x===selected?'selected':''}>${dateLabel(x)}</option>`).join(''); select.disabled=false;
}
function renderContracts() {
  const contracts=state.type==='call'?state.data.calls:state.data.puts, spot=state.data.spot;
  const select=$('contract'); select.innerHTML=contracts.map((c,i)=>`<option value="${i}">${c.strike.toFixed(2)} strike · ${money((c.bid+c.ask)/2||c.last)} · IV ${(c.impliedVolatility*100).toFixed(1)}%</option>`).join(''); select.disabled=!contracts.length;
  const nearest=contracts.reduce((best,c,i)=>Math.abs(c.strike-spot)<Math.abs(contracts[best]?.strike-spot)?i:best,0); select.value=String(nearest); state.contract=contracts[nearest]; updateContract();
}
function updateContract() {
  const c=state.contract; if(!c)return; $('contract-name').textContent=`${c.strike.toFixed(2)} ${state.type.toUpperCase()} · ${dateLabel(state.data.selectedExpiration)}`; $('bid-ask').textContent=`${money(c.bid)} / ${money(c.ask)}`; $('iv-value').textContent=`${(c.impliedVolatility*100).toFixed(1)}%`; $('oi-value').textContent=compact(c.openInterest);
  $('volatility').value=Math.min(200,Math.max(1,c.impliedVolatility*100)); updateLabels(); drawChart();
}
function updateLabels(){ $('vol-label').textContent=`${Number($('volatility').value).toFixed(0)}%`; $('rate-label').textContent=`${Number($('rate').value).toFixed(2)}%`; }
function drawChart() {
  if(!state.contract)return; const expiration=state.data.selectedExpiration, now=Date.now()/1000, days=Math.max(1,Math.ceil((expiration-now)/86400));
  const sigma=Number($('volatility').value)/100, r=Number($('rate').value)/100, currentSpot=state.data.spot, futureSpot=Math.max(.01,Number($('future-price').value)||currentSpot), K=state.contract.strike;
  const points=[]; for(let elapsed=0;elapsed<=days;elapsed++){ const remaining=Math.max(days-elapsed,1/365), spot=currentSpot+(futureSpot-currentSpot)*(elapsed/days); points.push({elapsed,remaining,spot,value:greeks(spot,K,remaining/365,r,sigma,state.type)[state.greek]}); }
  const svg=$('chart'), W=1000,H=430,m={l:75,r:25,t:25,b:48}, iw=W-m.l-m.r,ih=H-m.t-m.b; let min=Math.min(...points.map(p=>p.value)),max=Math.max(...points.map(p=>p.value)); if(min===max){min-=1;max+=1} const pad=(max-min)*.12;min-=pad;max+=pad;
  const x=p=>m.l+(p.elapsed/days)*iw,y=p=>m.t+(max-p.value)/(max-min)*ih,path=points.map((p,i)=>`${i?'L':'M'}${x(p).toFixed(2)},${y(p).toFixed(2)}`).join(' '),area=`${path} L${x(points.at(-1))},${m.t+ih} L${x(points[0])},${m.t+ih} Z`;
  let grid='';for(let i=0;i<=4;i++){const yy=m.t+ih*i/4,v=max-(max-min)*i/4;grid+=`<line class="axis" x1="${m.l}" y1="${yy}" x2="${W-m.r}" y2="${yy}"/><text class="axis-text" x="${m.l-12}" y="${yy+4}" text-anchor="end">${v.toFixed(greekMeta[state.greek].digits)}</text>`} for(let i=0;i<=4;i++){const xx=m.l+iw*i/4,rem=Math.round(days*(1-i/4));grid+=`<text class="axis-text" x="${xx}" y="${H-16}" text-anchor="middle">${rem}d remaining</text>`}
  svg.innerHTML=`<defs><linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#235c43" stop-opacity=".18"/><stop offset="1" stop-color="#235c43" stop-opacity="0"/></linearGradient></defs>${grid}<path class="area" d="${area}"/><path class="series" d="${path}"/><g id="focus" class="hidden"><line class="focus-line" y1="${m.t}" y2="${m.t+ih}"/><circle class="focus-dot" r="6"/></g><rect class="hit" x="${m.l}" y="${m.t}" width="${iw}" height="${ih}"/>`;
  $('chart-title').textContent=`${greekMeta[state.greek].label} through expiration`; $('model-note').textContent=`Price path ${money(currentSpot)} → ${money(futureSpot)} • IV ${(sigma*100).toFixed(0)}% constant • No dividends`;
  const hit=svg.querySelector('.hit'),focus=$('focus'),tip=$('tooltip'); hit.addEventListener('pointermove',e=>{const rect=svg.getBoundingClientRect(),px=(e.clientX-rect.left)*W/rect.width,idx=Math.max(0,Math.min(days,Math.round((px-m.l)/iw*days))),p=points[idx],xx=x(p),yy=y(p);focus.classList.remove('hidden');focus.querySelector('line').setAttribute('x1',xx);focus.querySelector('line').setAttribute('x2',xx);focus.querySelector('circle').setAttribute('cx',xx);focus.querySelector('circle').setAttribute('cy',yy);tip.classList.remove('hidden');tip.style.left=`${xx/W*100}%`;tip.style.top=`${yy/H*100}%`;tip.innerHTML=`${p.remaining} days remaining · Stock ${money(p.spot)}<br><strong>${greekMeta[state.greek].label} ${p.value.toFixed(greekMeta[state.greek].digits)}</strong>`}); hit.addEventListener('pointerleave',()=>{focus.classList.add('hidden');tip.classList.add('hidden')});
}

Object.keys(greekMeta).forEach(key=>{const b=document.createElement('button');b.textContent=greekMeta[key].label;b.dataset.greek=key;if(key===state.greek)b.classList.add('active');b.onclick=()=>{state.greek=key;document.querySelectorAll('.greek-tabs button').forEach(x=>x.classList.toggle('active',x.dataset.greek===key));drawChart()};$('greek-tabs').append(b)});
$('symbol-form').addEventListener('submit',e=>{e.preventDefault();loadChain($('symbol').value.trim().toUpperCase())});
$('expiration').addEventListener('change',e=>loadChain(state.data.symbol,e.target.value));
$('contract').addEventListener('change',e=>{const list=state.type==='call'?state.data.calls:state.data.puts;state.contract=list[Number(e.target.value)];updateContract()});
['call','put'].forEach(type=>$(type+'-button').addEventListener('click',()=>{state.type=type;document.querySelectorAll('.segmented button').forEach(b=>b.classList.toggle('active',b.dataset.type===type));renderContracts()}));
['volatility','rate'].forEach(id=>$(id).addEventListener('input',()=>{updateLabels();drawChart()}));
$('future-price-slider').addEventListener('input',()=>{$('future-price').value=Number($('future-price-slider').value).toFixed(2);drawChart()});
$('future-price').addEventListener('input',()=>{const value=Math.max(.01,Number($('future-price').value)||.01);if(value<Number($('future-price-slider').min))$('future-price-slider').min=Math.floor(value);if(value>Number($('future-price-slider').max))$('future-price-slider').max=Math.ceil(value);$('future-price-slider').value=value;drawChart()});
loadChain('AAPL');
