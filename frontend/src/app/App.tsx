import { useEffect, useState } from 'react';
import { AppNavbar } from '../components/AppNavbar';
import { ViewSwitcher } from '../components/ViewSwitcher';
import { EarningsCalendar } from '../features/earnings/components/EarningsCalendar';
import { EarningsHistory } from '../features/earnings-history/components/EarningsHistory';
import { OptionsTerminal } from '../features/options/components/OptionsTerminal';
import { MarketResearch } from '../features/research/components/MarketResearch';
import { PriceHistory } from '../features/price-history/components/PriceHistory';
import { StockWatchlist } from '../features/watchlist/components/StockWatchlist';
import { TickerResearch } from '../features/ticker-research/components/TickerResearch';
import { ResearchChat } from '../features/chat/components/ResearchChat';
import { SecurityCompare } from '../features/security-compare/components/SecurityCompare';
import { TradeJournal } from '../features/trade-journal/components/TradeJournal';
import { FocusBoard } from '../features/focus/components/FocusBoard';
import { StrategySimulator } from '../features/strategy-simulator/components/StrategySimulator';
import { HoldersView } from '../features/holders/components/HoldersView';
import { OptionChainView } from '../features/option-chain/components/OptionChainView';
import { NetWorthTracker } from '../features/net-worth/components/NetWorthTracker';
import { RealEstateResearch } from '../features/real-estate/components/RealEstateResearch';
import { OptionsEye } from '../features/eye/components/OptionsEye';
import { KellyCriterionLab } from '../features/kelly/components/KellyCriterionLab';
import { InvestmentSandbox } from '../features/sandbox/components/InvestmentSandbox';
import { DailyPerformanceEvaluator } from '../features/daily-performance/components/DailyPerformanceEvaluator';
import { useEnabledViews, type ViewId } from './viewPreferences';

const getPage = (): 'chain' | 'chat' | 'compare' | 'daily-performance' | 'eye' | 'earnings' | 'earnings-history' | 'focus' | 'holders' | 'journal' | 'kelly' | 'net-worth' | 'options' | 'price-history' | 'real-estate' | 'research' | 'sandbox' | 'simulator' | 'ticker' | 'watchlist' => window.location.hash === '#/chain' ? 'chain' : window.location.hash === '#/kelly' ? 'kelly' : window.location.hash === '#/chat' ? 'chat' : window.location.hash === '#/daily-performance' ? 'daily-performance' : window.location.hash === '#/compare' ? 'compare' : window.location.hash === '#/eye' ? 'eye' : window.location.hash === '#/focus' ? 'focus' : window.location.hash === '#/holders' ? 'holders' : window.location.hash === '#/net-worth' ? 'net-worth' : window.location.hash === '#/sandbox' ? 'sandbox' : window.location.hash === '#/simulator' ? 'simulator' : window.location.hash === '#/journal' ? 'journal' : window.location.hash === '#/earnings' ? 'earnings' : window.location.hash === '#/earnings-history' ? 'earnings-history' : window.location.hash === '#/price-history' ? 'price-history' : window.location.hash === '#/real-estate' ? 'real-estate' : window.location.hash === '#/research' ? 'research' : window.location.hash.startsWith('#/ticker/') ? 'ticker' : window.location.hash === '#/watchlist' ? 'watchlist' : 'options';
const getTicker=()=>decodeURIComponent(window.location.hash.split('/')[2]??'AAPL').toUpperCase();

export function App() {
  const embedded=new URLSearchParams(window.location.search).get('embed')==='1';
  const [page, setPage] = useState(getPage);
  const enabledViews=useEnabledViews();
  useEffect(() => { const update = () => setPage(getPage()); window.addEventListener('hashchange', update); return () => window.removeEventListener('hashchange', update); }, []);
  useEffect(()=>{if(embedded)return;const requested=(page==='ticker'?'research':page) as ViewId;if(!enabledViews.includes(requested))window.location.hash=`#/${enabledViews[0]}`},[page,enabledViews,embedded]);
  return <>{!embedded&&<AppNavbar activePage={page}/>}{page === 'chain' ? <OptionChainView/> : page === 'kelly' ? <KellyCriterionLab/> : page === 'chat' ? <ResearchChat/> : page === 'daily-performance' ? <DailyPerformanceEvaluator/> : page === 'compare' ? <SecurityCompare/> : page === 'eye' ? <OptionsEye/> : page === 'focus' ? <FocusBoard/> : page === 'holders' ? <HoldersView/> : page === 'net-worth' ? <NetWorthTracker/> : page === 'sandbox' ? <InvestmentSandbox/> : page === 'simulator' ? <StrategySimulator/> : page === 'journal' ? <TradeJournal/> : page === 'earnings' ? <EarningsCalendar/> : page === 'earnings-history' ? <EarningsHistory/> : page === 'price-history' ? <PriceHistory/> : page === 'real-estate' ? <RealEstateResearch/> : page === 'research' ? <MarketResearch/> : page === 'ticker' ? <TickerResearch symbol={getTicker()}/> : page === 'watchlist' ? <StockWatchlist/> : <OptionsTerminal/>}{!embedded&&<ViewSwitcher/>}</>;
}
